import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DOMES — Whole-Person Digital Twins",
  description:
    "The most comprehensive longitudinal representation of a single human life ever attempted.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-navy-900 text-gray-200">{children}</body>
    </html>
  );
}
