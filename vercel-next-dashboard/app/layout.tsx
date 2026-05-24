import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Premium Railway Operational Intelligence",
  description: "Command-center analytics for Indian premium passenger railway operations.",
  openGraph: {
    title: "Premium Railway Operational Intelligence",
    description: "Rajdhani, Vande Bharat, and premium corridor reliability intelligence.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
