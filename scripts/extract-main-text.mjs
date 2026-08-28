import fs from "node:fs";

const file = process.argv[2];
const html = fs.readFileSync(file, "utf8");

const mainMatch = html.match(/<main>([\s\S]*?)<\/main>/);
if (!mainMatch) {
  console.error("no <main> found in", file);
  process.exit(1);
}

let text = mainMatch[1]
  .replace(/<[^>]+>/g, " ")
  .replace(/&amp;/g, "&")
  .replace(/&lt;/g, "<")
  .replace(/&gt;/g, ">")
  .replace(/&quot;/g, '"')
  .replace(/&#39;/g, "'")
  .replace(/\s+/g, " ")
  .trim();

const titleMatch = html.match(/<title>([\s\S]*?)<\/title>/);
const title = titleMatch ? titleMatch[1].trim() : "";

console.log(JSON.stringify({ title, text }));
