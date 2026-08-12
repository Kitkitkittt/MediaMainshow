import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the Tier 1 house dashboard", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>Mainshow Tier 1 — House Dashboard<\/title>/i);
  assert.match(html, /DatVietVAC/);
  assert.match(html, /YeaH1/);
  assert.match(html, /667\.055\.502/);
  assert.match(html, /99<\/strong>/);
  assert.match(html, /Thiếu tập đã phát/);
  assert.match(html, /og\.png/);
  assert.doesNotMatch(html, /codex-preview|Your site is taking shape/);
});

test("ships source-synced Tier 1 data and accessible filters", async () => {
  const [page, layout, data] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/layout.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/data/tier1.json", import.meta.url), "utf8"),
  ]);
  const parsed = JSON.parse(data);

  assert.equal(parsed.seasons.length, 8);
  assert.equal(parsed.totals.episodes, 99);
  assert.equal(parsed.totals.missingAiredEpisodes, 0);
  assert.deepEqual(
    parsed.houses.map((house) => house.id),
    ["datvietvac", "yeah1"],
  );
  assert.match(page, /aria-pressed/);
  assert.match(page, /aria-label="Lọc theo nhà sản xuất"/);
  assert.match(layout, /Mainshow Tier 1 — Cuộc đua theo từng nhà/);
  assert.doesNotMatch(page, /SkeletonPreview|_sites-preview/);
});
