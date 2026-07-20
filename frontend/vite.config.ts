import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// GitHub Pagesは https://<user>.github.io/<repo>/ 配下で配信されるため、
// 本番ビルドのみサブパスをbaseに設定する。
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  base: mode === "production" ? "/design-news-digest/" : "/",
}));
