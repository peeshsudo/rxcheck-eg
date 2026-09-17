"use client";
import { useState } from "react";

const FOOD = [
  { id: "empty",  emoji: "🍽️", ar: "على معدة فارغة" },
  { id: "before", emoji: "🍞", ar: "قبل الأكل" },
  { id: "with",   emoji: "🥗", ar: "مع الأكل" },
  { id: "after",  emoji: "🍽️", ar: "بعد الأكل" },
];

export default function FoodSelector({ drug, times, onSubmit }: any) {
  const [food, setFood] = useState<string | null>(null);

  return (
    <div className="bg-white rounded-xl border p-4">
      <h2 className="font-bold mb-1">علاقة {drug.brand_ar} بالطعام</h2>
      <p className="text-xs text-[#7C8B85] mb-3">هل تتناوله قبل الأكل أم بعده؟</p>
      <div className="grid grid-cols-2 gap-2">
        {FOOD.map((f) => (
          <button
            key={f.id}
            onClick={() => setFood(f.id)}
            className={`p-3 rounded-lg border-2 flex flex-col items-center gap-1 ${
              food === f.id ? "border-[#0F5C56] bg-[#DCEDE9] font-bold" : "border-[#D8E3DF]"
            }`}
          >
            <span className="text-2xl">{f.emoji}</span>
            <span className="text-xs">{f.ar}</span>
          </button>
        ))}
      </div>
      <button
        onClick={() => onSubmit(food)}
        className="w-full mt-4 p-3 rounded-lg bg-[#0F5C56] text-white font-bold"
      >
        حفظ التذكير
      </button>
    </div>
  );
}