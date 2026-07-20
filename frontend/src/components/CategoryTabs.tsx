import { CATEGORY_LABELS, CATEGORY_ORDER, type Article, type CategoryCode } from "../types";

export type TabValue = "all" | CategoryCode;

interface Props {
  articles: Article[];
  activeTab: TabValue;
  onChange: (tab: TabValue) => void;
}

export default function CategoryTabs({ articles, activeTab, onChange }: Props) {
  const counts = new Map<TabValue, number>();
  counts.set("all", articles.length);
  for (const category of CATEGORY_ORDER) {
    counts.set(category, articles.filter((a) => a.categories.includes(category)).length);
  }

  const tabs: { value: TabValue; label: string }[] = [
    { value: "all", label: "すべて" },
    ...CATEGORY_ORDER.map((c) => ({ value: c as TabValue, label: CATEGORY_LABELS[c] })),
  ];

  return (
    <div className="category-tabs" role="tablist">
      {tabs.map((tab) => (
        <button
          key={tab.value}
          role="tab"
          aria-selected={activeTab === tab.value}
          className={`category-tabs__tab${activeTab === tab.value ? " is-active" : ""}`}
          onClick={() => onChange(tab.value)}
        >
          {tab.label}
          <span className="category-tabs__count">{counts.get(tab.value) ?? 0}</span>
        </button>
      ))}
    </div>
  );
}
