#!/usr/bin/env python3
"""毎朝のニュース収集バッチ。

固定RSSフィード + Google News キーワード検索RSS（無料・APIキー不要）から記事を集め、
カテゴリごとにルールベースで分類し、公開日ごとの JSON ファイルとして
frontend/public/data/ 配下に保存する。GitHub Actions から1日1回実行される想定。

要約は各フィードが提供する description をそのまま整形して使う（生成AIは使わない、無料方針）。
記事本文は保存せず、タイトル・出典・リンク・見出し要約のみを保持する（著作権配慮）。
"""
import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests

from feeds import FIXED_FEEDS, KEYWORD_QUERIES

JST = timezone(timedelta(hours=9))
USER_AGENT = "Mozilla/5.0 (compatible; DesignNewsDigestBot/1.0)"
REQUEST_TIMEOUT = 15
SUMMARY_MAX_LEN = 200
# RSSやGoogle Newsのキーワード検索は古い記事も混ざって返ってくるため、
# 直近N日分だけを「今日のダイジェスト」として取り込む。アーカイブは日々の実行の積み重ねで育つ。
RECENT_WINDOW_DAYS = 14

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "frontend" / "public" / "data"

TAG_RE = re.compile(r"<[^>]+>")


def clean_text(raw: str) -> str:
    if not raw:
        return ""
    text = TAG_RE.sub("", raw)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > SUMMARY_MAX_LEN:
        text = text[:SUMMARY_MAX_LEN].rstrip() + "…"
    return text


def google_news_rss_url(keyword: str) -> str:
    q = urllib.parse.quote(keyword)
    return f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja"


def fetch_feed(url: str):
    """1フィード分の取得・パース。失敗しても他フィードの処理は止めない。"""
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  [警告] 取得失敗: {url} ({exc})", file=sys.stderr)
        return None
    parsed = feedparser.parse(resp.content)
    if parsed.bozo and not parsed.entries:
        print(f"  [警告] パース失敗: {url} ({parsed.bozo_exception})", file=sys.stderr)
        return None
    return parsed


def extract_thumbnail(entry):
    media = entry.get("media_thumbnail") or entry.get("media_content")
    if media:
        url = media[0].get("url")
        if url:
            return url
    for link in entry.get("links", []):
        if str(link.get("type", "")).startswith("image/"):
            return link.get("href")
    return None


def extract_published(entry):
    parsed_time = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed_time:
        dt_utc = datetime.fromtimestamp(time.mktime(parsed_time), tz=timezone.utc)
        return dt_utc.astimezone(JST)
    return None


def make_id(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def build_article(entry, source_name, source_type, categories, matched_keyword=None):
    url = entry.get("link")
    if not url:
        return None
    title = clean_text(entry.get("title", ""))
    if not title:
        return None
    published = extract_published(entry)
    now = datetime.now(JST)
    summary = clean_text(entry.get("summary", "") or entry.get("description", ""))
    return {
        "id": make_id(url),
        "title": title,
        "url": url,
        "source_name": source_name,
        "source_type": source_type,
        "categories": categories,
        "summary": summary,
        "thumbnail_url": extract_thumbnail(entry),
        "published_at": (published or now).isoformat(),
        "fetched_at": now.isoformat(),
        "matched_keywords": [matched_keyword] if matched_keyword else [],
    }


def collect_articles():
    articles = []

    print("固定RSSフィードを取得中...")
    for feed in FIXED_FEEDS:
        print(f"  - {feed['name']} ({feed['url']})")
        parsed = fetch_feed(feed["url"])
        if not parsed:
            continue
        for entry in parsed.entries:
            article = build_article(entry, feed["name"], "fixed_rss", feed["categories"])
            if article:
                articles.append(article)

    print("キーワード検索(Google News RSS)を取得中...")
    for query in KEYWORD_QUERIES:
        keyword = query["keyword"]
        print(f"  - {keyword}")
        parsed = fetch_feed(google_news_rss_url(keyword))
        if not parsed:
            continue
        for entry in parsed.entries:
            source_name = keyword
            source = entry.get("source")
            if isinstance(source, dict) and source.get("title"):
                source_name = source["title"]
            article = build_article(
                entry, source_name, "keyword_search", query["categories"], matched_keyword=keyword
            )
            if article:
                articles.append(article)

    return articles


def filter_recent(articles, now):
    cutoff = now - timedelta(days=RECENT_WINDOW_DAYS)
    recent = []
    for article in articles:
        published = datetime.fromisoformat(article["published_at"])
        if published >= cutoff:
            recent.append(article)
    return recent


def bucket_by_date(articles):
    buckets = {}
    for article in articles:
        date_str = article["published_at"][:10]  # YYYY-MM-DD
        buckets.setdefault(date_str, []).append(article)
    return buckets


def merge_into_file(date_str: str, new_articles: list) -> int:
    """既存の日次ファイルとID(=URLのハッシュ)でマージし、重複を排除して保存する。"""
    path = DATA_DIR / f"{date_str}.json"
    existing_by_id = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            existing_by_id = {a["id"]: a for a in existing}
        except (json.JSONDecodeError, KeyError):
            existing_by_id = {}

    for article in new_articles:
        existing_by_id[article["id"]] = article

    merged = sorted(existing_by_id.values(), key=lambda a: a["published_at"], reverse=True)
    path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(merged)


def update_dates_index():
    dates = sorted((p.stem for p in DATA_DIR.glob("*.json") if p.stem != "dates"), reverse=True)
    (DATA_DIR / "dates.json").write_text(
        json.dumps(
            {"dates": dates, "updated_at": datetime.now(JST).isoformat()},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return dates


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    articles = collect_articles()
    print(f"取得記事数(重複含む): {len(articles)}")

    now = datetime.now(JST)
    recent_articles = filter_recent(articles, now)
    print(f"直近{RECENT_WINDOW_DAYS}日分に絞り込み: {len(recent_articles)} 件")

    buckets = bucket_by_date(recent_articles)
    for date_str, day_articles in sorted(buckets.items()):
        total = merge_into_file(date_str, day_articles)
        print(f"  {date_str}: 新規/更新 {len(day_articles)} 件 -> 合計 {total} 件")

    dates = update_dates_index()
    print(f"アーカイブ日数: {len(dates)} 日分 (最新: {dates[0] if dates else 'なし'})")


if __name__ == "__main__":
    main()
