"use client";
import { CheckSquare } from "lucide-react";

export default function CurationPanel() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold">Curation</h1>
      <p className="text-sm text-slate-500 mt-1">Pharmacist review queue — approve, reject, or annotate proposals.</p>
      <div className="mt-8 flex items-center justify-center border-2 border-dashed border-slate-200 rounded-2xl py-16 text-slate-300">
        <CheckSquare size={48} />
      </div>
    </div>
  );
}