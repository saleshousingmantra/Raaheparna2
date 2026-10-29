// Copies the static site into dist/ for Hostinger (output directory: dist).
// No dependencies and no compilation: the site is plain HTML/CSS/JS.
import { rmSync, mkdirSync, cpSync, existsSync } from "node:fs";

const OUT = "dist";
// Only these files and folders are published.
const SITE = [
  "index.html",
  "404.html",
  "thank-you",
  "blog",
  "js",
  "images",
  "favicon.ico",
  "favicon-16x16.png",
  "favicon-32x32.png",
  "favicon-48x48.png",
  "favicon-96x96.png",
  "apple-touch-icon.png",
  "icon-192.png",
  "icon-512.png",
  "site.webmanifest",
  "robots.txt",
  "sitemap.xml",
  ".htaccess",
];

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT);

for (const entry of SITE) {
  if (!existsSync(entry)) continue; // optional files
  cpSync(entry, `${OUT}/${entry}`, { recursive: true });
}

if (!existsSync(`${OUT}/index.html`)) {
  console.error("Build failed: index.html missing from dist/");
  process.exit(1);
}
console.log("Built dist/ for Hostinger.");
