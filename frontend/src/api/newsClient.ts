import type { Article, DatesIndex } from "../types";

const dataUrl = (path: string) => `${import.meta.env.BASE_URL}data/${path}`;

export async function fetchDatesIndex(): Promise<DatesIndex> {
  const res = await fetch(dataUrl("dates.json"));
  if (!res.ok) {
    throw new Error("日付一覧の取得に失敗しました");
  }
  return res.json();
}

export async function fetchArticlesByDate(date: string): Promise<Article[]> {
  const res = await fetch(dataUrl(`${date}.json`));
  if (!res.ok) {
    throw new Error(`${date} の記事の取得に失敗しました`);
  }
  return res.json();
}
