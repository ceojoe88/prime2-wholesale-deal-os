import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Prime 2 Wholesale Deal OS",
  description: "Private operator-only wholesale real estate command center"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
