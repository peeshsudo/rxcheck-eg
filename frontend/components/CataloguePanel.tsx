"use client";
import { AlignLeft } from "lucide-react";

export default function CataloguePanel() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold">Catalogue</h1>
      <p className="text-sm text-slate-500 mt-1">Browse the curated drug and food registry.</p>
      <div className="mt-8 flex items-center justify-center border-2 border-dashed border-slate-200 rounded-2xl py-16 text-slate-300">
        <AlignLeft size={48} />
      </div>
    </div>
  );
}