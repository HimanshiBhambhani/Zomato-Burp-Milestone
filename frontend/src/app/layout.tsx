import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BURP - AI Restaurant Recommender",
  description: "Discover your perfect restaurant with AI-powered recommendations",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
