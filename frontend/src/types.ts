export type CategoryCode =
  | "space_design"
  | "architecture_interior"
  | "exhibition_expo"
  | "sustainable_material";

export type SourceType = "fixed_rss" | "keyword_search";

export interface Article {
  id: string;
  title: string;
  url: string;
  source_name: string;
  source_type: SourceType;
  categories: CategoryCode[];
  summary: string;
  thumbnail_url: string | null;
  published_at: string;
  fetched_at: string;
  matched_keywords: string[];
}

export interface DatesIndex {
  dates: string[];
  updated_at: string;
}

export const CATEGORY_ORDER: CategoryCode[] = [
  "space_design",
  "architecture_interior",
  "exhibition_expo",
  "sustainable_material",
];

export const CATEGORY_LABELS: Record<CategoryCode, string> = {
  space_design: "空間デザイン・ディスプレイ",
  architecture_interior: "建築・インテリア",
  exhibition_expo: "展示会・万博",
  sustainable_material: "素材・サステナブル",
};
