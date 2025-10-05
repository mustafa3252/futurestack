import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "./markdown.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "StartupScout - AI-Powered Startup Validation | Cerebras + Llama 4",
  description: "Validate your startup ideas in minutes with ultra-fast AI agents powered by Cerebras inference and Meta's Llama 4 Maverick",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
