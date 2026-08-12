import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parse } from "csv-parse/sync";

const dashboardRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const projectRoot = resolve(dashboardRoot, "..");

const showCatalog = {
  ATSH: {
    houseId: "datvietvac",
    house: "DatVietVAC",
    shortName: "Anh Trai Say Hi",
  },
  EXSH: {
    houseId: "datvietvac",
    house: "DatVietVAC",
    shortName: "Em Xinh Say Hi",
  },
  THSH: {
    houseId: "datvietvac",
    house: "DatVietVAC",
    shortName: "Tinh Hà Say Hi",
  },
  ATVNCG: {
    houseId: "yeah1",
    house: "YeaH1",
    shortName: "Anh Trai Vượt Ngàn Chông Gai",
  },
  CDDG: {
    houseId: "yeah1",
    house: "YeaH1",
    shortName: "Chị Đẹp Đạp Gió",
  },
};

const houseCatalog = {
  datvietvac: {
    id: "datvietvac",
    name: "DatVietVAC",
    channel: "Vie Channel / HTV2 / VieON",
    description: "Hệ sinh thái Say Hi",
  },
  yeah1: {
    id: "yeah1",
    name: "YeaH1",
    channel: "YEAH1 SHOW / VTV3",
    description: "Hệ sinh thái Chông Gai & Chị Đẹp",
  },
};

function readCsv(filename) {
  return parse(readFileSync(resolve(projectRoot, "outputs", filename), "utf8"), {
    bom: true,
    columns: true,
    skip_empty_lines: true,
  });
}

function integer(value) {
  if (value === "" || value === null || value === undefined) return null;
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) ? parsed : null;
}

const seasonRows = readCsv("season_summary.csv")
  .filter((row) => showCatalog[row.show_id])
  .map((row) => {
    const show = showCatalog[row.show_id];
    return {
      showId: row.show_id,
      showName: show.shortName,
      seasonId: row.season_id,
      year: integer(row.season_year),
      status: row.season_status,
      houseId: show.houseId,
      house: show.house,
      expectedEpisodes: integer(row.expected_episode_count),
      episodes: integer(row.canonical_episode_count) ?? 0,
      missingAiredEpisodes: integer(row.missing_episode_count) ?? 0,
      totalViews: integer(row.total_views) ?? 0,
      averageViews: integer(row.average_views) ?? 0,
      medianViews: integer(row.median_views) ?? 0,
      peakEpisode: integer(row.max_episode_no),
      peakViews: integer(row.max_episode_views) ?? 0,
      firstFiveViews: integer(row.first_5_total_views),
      qcStatus: row.qc_status,
      snapshotAt: row.snapshot_at,
    };
  })
  .sort((a, b) => b.totalViews - a.totalViews);

const episodeRows = readCsv("episode_registry.csv")
  .filter(
    (row) => showCatalog[row.show_id] && row.canonical_flag.toLowerCase() === "true",
  )
  .map((row) => {
    const show = showCatalog[row.show_id];
    return {
      showId: row.show_id,
      showName: show.shortName,
      seasonId: row.season_id,
      houseId: show.houseId,
      house: show.house,
      episode: integer(row.episode_no),
      title: row.title,
      views: integer(row.view_count) ?? 0,
      publishedAt: row.published_at,
      videoUrl: row.video_url,
      channel: row.channel_name.trim(),
    };
  })
  .sort((a, b) => b.views - a.views);

const houses = Object.values(houseCatalog).map((house) => {
  const seasons = seasonRows.filter((season) => season.houseId === house.id);
  const totalViews = seasons.reduce((sum, season) => sum + season.totalViews, 0);
  const episodes = seasons.reduce((sum, season) => sum + season.episodes, 0);
  return {
    ...house,
    seasonCount: seasons.length,
    showCount: new Set(seasons.map((season) => season.showId)).size,
    episodes,
    totalViews,
    averageViewsPerEpisode: episodes ? Math.round(totalViews / episodes) : 0,
    airingCount: seasons.filter((season) => season.status === "airing").length,
  };
});

const totalViews = houses.reduce((sum, house) => sum + house.totalViews, 0);
const totalEpisodes = houses.reduce((sum, house) => sum + house.episodes, 0);
for (const house of houses) {
  house.share = totalViews ? Math.round((house.totalViews / totalViews) * 1000) / 10 : 0;
}

const snapshotAt = seasonRows
  .map((season) => season.snapshotAt)
  .filter(Boolean)
  .sort()
  .at(-1);

const payload = {
  snapshotAt,
  totals: {
    views: totalViews,
    episodes: totalEpisodes,
    seasons: seasonRows.length,
    shows: new Set(seasonRows.map((season) => season.showId)).size,
    missingAiredEpisodes: seasonRows.reduce(
      (sum, season) => sum + season.missingAiredEpisodes,
      0,
    ),
  },
  houses,
  seasons: seasonRows,
  topEpisodes: episodeRows.slice(0, 30),
  methodology: {
    metric: "Lượt xem tích lũy trên video full main-show chính thức",
    exclusion: "Không gồm performance, concert, BTS, cut, reaction hoặc fan upload",
    audienceCaveat: "Lượt xem không tương đương người xem duy nhất",
  },
};

const output = resolve(dashboardRoot, "app", "data", "tier1.json");
mkdirSync(dirname(output), { recursive: true });
writeFileSync(output, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
console.log(`Synced ${seasonRows.length} Tier 1 seasons and ${episodeRows.length} episodes.`);
