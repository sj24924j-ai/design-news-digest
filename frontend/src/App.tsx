import { useEffect, useMemo, useState } from "react";
import "./App.css";
import Header from "./components/Header";
import CategoryTabs, { type TabValue } from "./components/CategoryTabs";
import ArticleList from "./components/ArticleList";
import { fetchArticlesByDate, fetchDatesIndex } from "./api/newsClient";
import type { Article } from "./types";

export default function App() {
  const [dates, setDates] = useState<string[]>([]);
  const [updatedAt, setUpdatedAt] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [articles, setArticles] = useState<Article[]>([]);
  const [activeTab, setActiveTab] = useState<TabValue>("all");
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    fetchDatesIndex()
      .then((index) => {
        setDates(index.dates);
        setUpdatedAt(index.updated_at);
        setSelectedDate(index.dates[0] ?? null);
        if (index.dates.length === 0) {
          setStatus("ready");
        }
      })
      .catch((err: Error) => {
        setErrorMessage(err.message);
        setStatus("error");
      });
  }, []);

  useEffect(() => {
    if (!selectedDate) return;
    setStatus("loading");
    fetchArticlesByDate(selectedDate)
      .then((data) => {
        setArticles(data);
        setStatus("ready");
      })
      .catch((err: Error) => {
        setErrorMessage(err.message);
        setStatus("error");
      });
  }, [selectedDate]);

  const filteredArticles = useMemo(() => {
    if (activeTab === "all") return articles;
    return articles.filter((a) => a.categories.includes(activeTab));
  }, [articles, activeTab]);

  if (status === "error") {
    return (
      <div className="app-shell">
        <p className="app-error">データの読み込みに失敗しました: {errorMessage}</p>
      </div>
    );
  }

  if (dates.length === 0 && status === "ready") {
    return (
      <div className="app-shell">
        <header className="app-header">
          <h1>デザインニュース ダイジェスト</h1>
        </header>
        <p className="app-empty">まだニュースデータがありません。バッチの初回実行をお待ちください。</p>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Header
        dates={dates}
        selectedDate={selectedDate ?? ""}
        isLatest={selectedDate === dates[0]}
        updatedAt={updatedAt}
        onChangeDate={setSelectedDate}
      />
      <CategoryTabs articles={articles} activeTab={activeTab} onChange={setActiveTab} />
      <main>
        {status === "loading" ? (
          <p className="app-loading">読み込み中...</p>
        ) : (
          <ArticleList articles={filteredArticles} />
        )}
      </main>
    </div>
  );
}
