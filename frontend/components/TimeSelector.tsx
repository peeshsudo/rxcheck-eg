"use client";
import { useState } from "react";
import { Sunrise, Sun, SunDim, CloudSun, Sunset, Moon, MoonStar } from "lucide-react";

const TIME_ICONS = [
  { id: "fajr",    label: "Fajr",    Icon: Sunrise },
  { id: "morning", label: "Morning", Icon: Sun },
  { id: "noon",    label: "Noon",    Icon: SunDim },
  { id: "asr",     label: "Asr",     Icon: CloudSun },
  { id: "maghrib", label: "Maghrib", Icon: Sunset },
  { id: "isha",    label: "Isha",    Icon: Moon },
  { id: "night",   label: "Night",   Icon: MoonStar },
];

export default function TimeSelector({ drug, onNext }: any) {
  const [selected, setSelected] = useState<string[]>([]);
  const name = drug?.generic_ar || drug?.generic_en || "الدواء";

  function toggle(id: string) {
    setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-4">
      <h2 className="font-bold mb-1 text-slate-900">When to take {drug?.generic_en}؟</h2>
      <p className="text-xs text-slate-500 mb-4">Pick one or more times</p>
      <div className="grid grid-cols-4 gap-2">
        {TIME_ICONS.map(({ id, label, Icon }) => {
          const on = selected.includes(id);
          return (
            <button
              key={id}
              onClick={() => toggle(id)}
              className={`aspect-square rounded-xl border-2 flex flex-col items-center justify-center gap-1 transition ${
                on
                  ? "border-teal-600 bg-teal-50 text-teal-800"
                  : "border-slate-200 bg-white text-slate-500 hover:border-slate-300"
              }`}
            >
              <Icon size={26} strokeWidth={on ? 2.2 : 1.8} />
              <span className="text-[10px] font-medium">{label}</span>
            </button>
          );
        })}
      </div>
      <button
        disabled={selected.length === 0}
        onClick={() => onNext(selected)}
        className="w-full mt-4 p-3 rounded-xl bg-teal-700 text-white font-bold disabled:opacity-40 transition"
      >
        Next
      </button>
    </div>
  );
}