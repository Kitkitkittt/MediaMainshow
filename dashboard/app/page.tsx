"use client";

import { useMemo, useState } from "react";
import data from "./data/tier1.json";

type HouseFilter = "all" | "datvietvac" | "yeah1";

const filters: { id: HouseFilter; label: string }[] = [
  { id: "all", label: "Tất cả" },
  { id: "datvietvac", label: "Nhà DatVietVAC" },
  { id: "yeah1", label: "Nhà YeaH1" },
];

const compact = new Intl.NumberFormat("vi-VN", {
  notation: "compact",
  maximumFractionDigits: 1,
});

const integer = new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 0 });

function viewLabel(value: number) {
  return `${compact.format(value)} views`;
}

function dateLabel(value: string) {
  return new Intl.DateTimeFormat("vi-VN", {
    dateStyle: "long",
    timeZone: "Asia/Ho_Chi_Minh",
  }).format(new Date(value));
}

export default function Home() {
  const [activeHouse, setActiveHouse] = useState<HouseFilter>("all");

  const seasons = useMemo(
    () =>
      activeHouse === "all"
        ? data.seasons
        : data.seasons.filter((season) => season.houseId === activeHouse),
    [activeHouse],
  );

  const episodes = useMemo(
    () =>
      data.topEpisodes
        .filter(
          (episode) => activeHouse === "all" || episode.houseId === activeHouse,
        )
        .slice(0, 10),
    [activeHouse],
  );

  const filteredViews = seasons.reduce((sum, season) => sum + season.totalViews, 0);
  const maxSeasonViews = Math.max(...seasons.map((season) => season.totalViews), 1);

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Mainshow Intelligence, về đầu trang">
          <span className="brand-mark">M</span>
          <span>
            MAINSHOW
            <small>INTELLIGENCE</small>
          </span>
        </a>
        <div className="snapshot-pill">
          <span className="live-dot" /> Snapshot · {dateLabel(data.snapshotAt)}
        </div>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow">Vietnam Entertainment · Tier 1</p>
          <h1>
            Cuộc đua main-show,
            <span> nhìn theo từng “nhà”.</span>
          </h1>
          <p className="hero-deck">
            So sánh sức xem full episode giữa hệ sinh thái DatVietVAC và YeaH1 —
            cùng một chuẩn dữ liệu, không lẫn performance, concert hay cut.
          </p>
        </div>
        <div className="hero-orbit" aria-hidden="true">
          <div className="orbit-ring ring-one" />
          <div className="orbit-ring ring-two" />
          <div className="orbit-core">
            <strong>{compact.format(data.totals.views)}</strong>
            <span>total views</span>
          </div>
        </div>
      </section>

      <section className="score-strip" aria-label="Tổng quan Tier 1">
        <article>
          <span>Tổng lượt xem</span>
          <strong>{integer.format(data.totals.views)}</strong>
        </article>
        <article>
          <span>Full episodes</span>
          <strong>{data.totals.episodes}</strong>
        </article>
        <article>
          <span>Mùa / chương trình</span>
          <strong>
            {data.totals.seasons} <small>/ {data.totals.shows}</small>
          </strong>
        </article>
        <article className="gap-score">
          <span>Thiếu tập đã phát</span>
          <strong>{data.totals.missingAiredEpisodes}</strong>
        </article>
      </section>

      <section className="section house-section" id="houses">
        <div className="section-heading">
          <div>
            <p className="eyebrow">House split</p>
            <h2>Hai hệ sinh thái, hai cấu trúc sức xem</h2>
          </div>
          <div className="filter-tabs" role="group" aria-label="Lọc theo nhà sản xuất">
            {filters.map((filter) => (
              <button
                key={filter.id}
                type="button"
                aria-pressed={activeHouse === filter.id}
                className={activeHouse === filter.id ? "active" : ""}
                onClick={() => setActiveHouse(filter.id)}
              >
                {filter.label}
              </button>
            ))}
          </div>
        </div>

        <div className="house-grid">
          {data.houses.map((house) => (
            <button
              type="button"
              key={house.id}
              onClick={() =>
                setActiveHouse(activeHouse === house.id ? "all" : (house.id as HouseFilter))
              }
              aria-pressed={activeHouse === house.id}
              className={`house-card ${house.id} ${activeHouse === house.id ? "selected" : ""}`}
            >
              <span className="house-index">0{data.houses.indexOf(house) + 1}</span>
              <span className="house-kicker">{house.description}</span>
              <strong className="house-name">{house.name}</strong>
              <span className="house-channel">{house.channel}</span>
              <span className="house-metric">
                <b>{compact.format(house.totalViews)}</b> lượt xem
              </span>
              <span className="share-row">
                <span>Thị phần lượt xem Tier 1</span>
                <b>{house.share}%</b>
              </span>
              <span className="share-track" aria-hidden="true">
                <i style={{ width: `${house.share}%` }} />
              </span>
              <span className="house-foot">
                {house.showCount} show · {house.seasonCount} mùa · {house.episodes} tập
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="section season-section" id="seasons">
        <div className="section-heading aligned">
          <div>
            <p className="eyebrow">Season scoreboard</p>
            <h2>{activeHouse === "all" ? "Xếp hạng 8 mùa Tier 1" : `Bảng mùa · ${seasons[0]?.house}`}</h2>
          </div>
          <p className="section-stat">
            <strong>{compact.format(filteredViews)}</strong>
            views trong bộ lọc
          </p>
        </div>

        <div className="season-list">
          {seasons.map((season, index) => (
            <article className={`season-row ${season.houseId}`} key={season.seasonId}>
              <span className="rank">{String(index + 1).padStart(2, "0")}</span>
              <div className="season-identity">
                <span className="house-tag">{season.house}</span>
                <h3>{season.showName}</h3>
                <p>
                  {season.year} · {season.status === "airing" ? "Đang phát" : "Hoàn tất"}
                </p>
              </div>
              <div className="season-bar-wrap">
                <div className="season-bar-label">
                  <span>{season.episodes}/{season.expectedEpisodes} tập</span>
                  <b>{viewLabel(season.totalViews)}</b>
                </div>
                <div className="season-bar">
                  <i style={{ width: `${(season.totalViews / maxSeasonViews) * 100}%` }} />
                </div>
              </div>
              <div className="season-detail">
                <span>TB / tập</span>
                <b>{compact.format(season.averageViews)}</b>
                <span>Peak</span>
                <b>E{season.peakEpisode} · {compact.format(season.peakViews)}</b>
              </div>
              <span className={`status ${season.status}`}>
                {season.status === "airing" ? "LIVE" : season.qcStatus}
              </span>
            </article>
          ))}
        </div>
      </section>

      <section className="section episode-section" id="episodes">
        <div className="section-heading aligned">
          <div>
            <p className="eyebrow">Episode leaderboard</p>
            <h2>Top full episode theo lượt xem</h2>
          </div>
          <p className="table-note">Bấm tiêu đề để mở video chính thức</p>
        </div>

        <div className="episode-table" role="table" aria-label="Top episode Tier 1">
          <div className="episode-head" role="row">
            <span>#</span>
            <span>Episode</span>
            <span>Nhà</span>
            <span>Lượt xem</span>
          </div>
          {episodes.map((episode, index) => (
            <div className="episode-row" role="row" key={`${episode.seasonId}-${episode.episode}`}>
              <span className="episode-rank">{String(index + 1).padStart(2, "0")}</span>
              <div>
                <a href={episode.videoUrl} target="_blank" rel="noreferrer">
                  {episode.showName} · Tập {episode.episode}
                </a>
                <small>{episode.seasonId}</small>
              </div>
              <span className={`mini-house ${episode.houseId}`}>{episode.house}</span>
              <strong>{integer.format(episode.views)}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="method-section">
        <div>
          <p className="eyebrow">Read this right</p>
          <h2>Đây là sức xem video, không phải rating TV.</h2>
        </div>
        <div className="method-grid">
          <p><span>01</span>{data.methodology.metric}.</p>
          <p><span>02</span>{data.methodology.exclusion}.</p>
          <p><span>03</span>{data.methodology.audienceCaveat}.</p>
        </div>
      </section>

      <footer>
        <span>Mainshow Tier 1 · Auditable YouTube Dataset</span>
        <span>Data cutoff: {dateLabel(data.snapshotAt)}</span>
      </footer>
    </main>
  );
}
