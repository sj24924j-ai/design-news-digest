import { CATEGORY_LABELS, type Article } from "../types";

function formatPublished(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleString("ja-JP", {
    month: "numeric",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function ArticleCard({ article }: { article: Article }) {
  return (
    <a className="article-card" href={article.url} target="_blank" rel="noreferrer noopener">
      {article.thumbnail_url && (
        <img
          className="article-card__thumb"
          src={article.thumbnail_url}
          alt=""
          loading="lazy"
        />
      )}
      <div className="article-card__body">
        <div className="article-card__meta">
          <span className="article-card__source">{article.source_name}</span>
          <span className="article-card__date">{formatPublished(article.published_at)}</span>
        </div>
        <h3 className="article-card__title">{article.title}</h3>
        {article.summary && <p className="article-card__summary">{article.summary}</p>}
        <div className="article-card__tags">
          {article.categories.map((c) => (
            <span key={c} className="article-card__tag">
              {CATEGORY_LABELS[c]}
            </span>
          ))}
        </div>
      </div>
    </a>
  );
}
