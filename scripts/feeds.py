"""固定RSSフィードとキーワード検索の設定。

要件定義書（requirements.md）4.1のカテゴリに対応させている。
カテゴリコード:
  space_design            空間デザイン・ディスプレイ
  architecture_interior   建築・インテリアデザイン
  exhibition_expo         イベント・展示会・万博
  sustainable_material    素材・サステナブル
"""

# 固定RSSフィード購読先。日本語ソースをメインとする方針のため、日本語メディアのみを採用する
# （英語圏メディアは原則キーワード検索側でも日本語記事のみ拾うようフィルタしている）。
# 実装時に疎通確認済みのものを採用。カバーしきれない分野は KEYWORD_QUERIES で補完する。
# 未決事項（requirements.md 13章）: 最終的な購読メディアは本人ヒアリング後に見直す。
FIXED_FEEDS = [
    {
        "name": "AXIS",
        "url": "https://www.axismag.jp/feed/",
        "categories": ["space_design", "architecture_interior"],
    },
    {
        "name": "10+1 website",
        "url": "https://10plus1.jp/feed/",
        "categories": ["architecture_interior"],
    },
    {
        "name": "大阪・関西万博公式ニュース",
        "url": "https://www.expo2025.or.jp/feed/",
        "categories": ["exhibition_expo"],
    },
    {
        "name": "丹青社",
        "url": "https://www.tanseisha.co.jp/feed/",
        "categories": ["space_design"],
    },
]

# Google News キーワード検索RSS（無料・APIキー不要）で補完する検索語。
# クエリは https://news.google.com/rss/search?q=<keyword>&hl=ja&gl=JP&ceid=JP:ja の形で組み立てる。
KEYWORD_QUERIES = [
    {"keyword": "乃村工藝社", "categories": ["space_design"]},
    {"keyword": "丹青社", "categories": ["space_design"]},
    {"keyword": "空間デザイン", "categories": ["space_design"]},
    {"keyword": "ディスプレイ業界 デザイン", "categories": ["space_design"]},
    {"keyword": "商業施設 デザイン", "categories": ["space_design", "architecture_interior"]},
    {"keyword": "建築デザイン トレンド", "categories": ["architecture_interior"]},
    {"keyword": "インテリアデザイン トレンド", "categories": ["architecture_interior"]},
    {"keyword": "展示会 業界 動向", "categories": ["exhibition_expo"]},
    {"keyword": "万博 パビリオン", "categories": ["exhibition_expo"]},
    {"keyword": "MICE 展示会", "categories": ["exhibition_expo"]},
    {"keyword": "サステナブル建材", "categories": ["sustainable_material"]},
    {"keyword": "新素材 内装", "categories": ["sustainable_material"]},
]

CATEGORY_LABELS = {
    "space_design": "空間デザイン・ディスプレイ",
    "architecture_interior": "建築・インテリア",
    "exhibition_expo": "展示会・万博",
    "sustainable_material": "素材・サステナブル",
}
