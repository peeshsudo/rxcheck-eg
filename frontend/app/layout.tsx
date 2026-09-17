import type { Metadata } from "next";
import { Noto_Kufi_Arabic, Inter } from "next/font/google";
import "./globals.css";

const kufi = Noto_Kufi_Arabic({ subsets: ["arabic"], variable: "--font-ar" });
const inter = Inter({ subsets: ["latin"], variable: "--font-en" });

export const metadata: Metadata = {
  title: "RxCheck EG",
  description: "فاحص تفاعلات الأدوية",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl" className={`${kufi.variable} ${inter.variable}`}>
      <body className="bg-[#EEF3F1] text-[#16231F] font-ar">{children}</body>
    </html>
  );
}