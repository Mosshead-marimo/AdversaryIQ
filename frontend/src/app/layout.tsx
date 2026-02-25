import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PyDetonator Dashboard",
  description: "Dynamic malware analysis and reporting dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
