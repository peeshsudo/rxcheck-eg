"use client";
import { useState } from "react";
import { Coffee, Utensils, UtensilsCrossed, Cookie } from "lucide-react";

const FOOD = [
  { id: "empty",  label: "Empty stomach", Icon: Coffee },
  { id: "before", label: "Before meal",   Icon: Utensils },
  { id: "with",   label: "With meal",     Icon: UtensilsCrossed },
  { id: "after",  label: "After meal",    Icon: Cookie },
];

export default function FoodSelector({ drug, times, onSubmit }: any) {
  const [food, setFood] = useState<string | null>(null);
  const name = drug?.generic_ar || drug?.generic_en || "الدواء";

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-4">
      <h2 className="font-bold mb-1 text-slate-900">Food relation for {name}</h2>
      <p className="text-xs text-slate-500 mb-4">Take before, with, or after food?</p>
      <div className="grid grid-cols-2 gap-3">
        {FOOD.map(({ id, label, Icon }) => {
          const on = food === id;
          return (
            <button
              key={id}
              onClick={() => setFood(id)}
              className={`p-4 rounded-xl border-2 flex flex-col items-center gap-2 transition ${
                on
                  ? "border-teal-600 bg-teal-50 text-teal-800"
                  : "border-slate-200 bg-white text-slate-500 hover:border-slate-300"
              }`}
            >
              <Icon size={26} strokeWidth={on ? 2.2 : 1.8} />
              <span className="text-xs font-medium">{label}</span>
            </button>
          );
        })}
      </div>
      <button
        onClick={() => onSubmit(food)}
        className="w-full mt-4 p-3 rounded-xl bg-teal-700 text-white font-bold transition"
      >
        Save reminder
      </button>
    </div>
  );
}