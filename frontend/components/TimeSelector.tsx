"use client";
import { useState } from "react";

const TIME_ICONS = [
  { id: "fajr",    emoji: "🌅", ar: "فجر" },
  { id: "morning", emoji: "🌄", ar: "صباح" },
  { id: "noon",    emoji: "☀️", ar: "ظهر" },
  { id: "asr",     emoji: "🌤️", ar: "عصر" },
  { id: "maghrib", emoji: "🌇", ar: "مغرب" },
  { id: "isha",    emoji: "🌙", ar: "عشاء" },
  { id: "night",   emoji: "🌑", ar: "ليل" },
];

export default function TimeSelector({ drug, onNext }: any) {
  const [selected, setSelected] = useState<string[]>([]);

  function toggle(id: string) {
    setSelected((s) => s.includes(id) ? s.filter((x) => x !== id) : [...s, id]);
  }

  return (
    <div className="bg-white rounded-xl border p-4">
      <h2 className="font-bold mb-1">متى تتناول {drug.brand_ar}؟</h2>
      <p className="text-xs text-[#7C8B85] mb-3">اختر وقتاً أو أكثر</p>
      <div className="grid grid-cols-4 gap-2">
        {TIME_ICONS.map((t) => (
          <button
            key={t.id}
            onClick={() => toggle(t.id)}
            className={`aspect-square rounded-xl border-2 flex flex-col items-center justify-center gap-1 ${
              selected.includes(t.id)
                ? "border-[#0F5C56] bg-[#DCEDE9]"
                : "border-[#D8E3DF] bg-white"
            }`}
          >
            <span className="text-2xl">{t.emoji}</span>
            <span className="text-[10px]">{t.ar}</span>
          </button>
        ))}
      </div>
      <button
        disabled={selected.length === 0}
        onClick={() => onNext(selected)}
        className="w-full mt-4 p-3 rounded-lg bg-[#0F5C56] text-white font-bold disabled:opacity-40"
      >
        التالي
      </button>
    </div>
  );
}