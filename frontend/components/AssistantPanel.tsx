"use client";
import { MessageCircle } from "lucide-react";

export default function AssistantPanel() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold">Assistant</h1>
      <p className="text-sm text-slate-500 mt-1">Coming soon — grounded Q&amp;A over the drug catalogue.</p>
      <div className="mt-8 flex items-center justify-center border-2 border-dashed border-slate-200 rounded-2xl py-16 text-slate-300">
        <MessageCircle size={48} />
      </div>
    </div>
  );
}