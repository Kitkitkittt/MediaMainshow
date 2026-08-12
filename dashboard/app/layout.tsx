import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mainshow Tier 1 — House Dashboard",
  description:
    "Dashboard so sánh sức xem Tier 1 giữa DatVietVAC và YeaH1 từ các full episode YouTube chính thức.",
  metadataBase: new URL("https://mainshow-tier1.pages.dev"),
  openGraph: {
    title: "Mainshow Tier 1 — Cuộc đua theo từng nhà",
    description: "DatVietVAC 70,8% · YeaH1 29,2% · 667 triệu lượt xem full episode.",
    images: [{ url: "/og.png", width: 1733, height: 909 }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Mainshow Tier 1 — Cuộc đua theo từng nhà",
    description: "DatVietVAC 70,8% · YeaH1 29,2% · 667 triệu lượt xem full episode.",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
