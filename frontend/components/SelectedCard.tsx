"use client";
import { useState } from "react";
import {
  Sunrise, Sun, SunDim, CloudSun, Sunset, Moon, MoonStar,
  Coffee, Utensils, UtensilsCrossed, Cookie,
  X, Check, Pencil,
} from "lucide-react";
import type { SelectedItem } from "./CheckPanel";

const TIMES = [
  { id: "fajr",    label: "Fajr",    Icon: Sunrise },
  { id: "morning", label: "Morning", Icon: Sun },
  { id: "noon",    label: "Noon",    Icon: SunDim },
  { id: "asr",     label: "Asr",     Icon: CloudSun },
  { id: "maghrib", label: "Maghrib", Icon: Sunset },
  { id: "isha",    label: "Isha",    Icon: Moon },
  { id: "night",   label: "Night",   Icon: MoonStar },
];

const FOODS = [
  { id: "empty",  label: "Empty stomach", Icon: Coffee },
  { id: "before", label: "Before meal",   Icon: Utensils },
  { id: "with",   label: "With meal",     Icon: UtensilsCrossed },
  { id: "after",  label: "After meal",    Icon: Cookie },
];

function labelForTime(id: string) {
  return TIMES.find((t) => t.id === id)?.label ?? id;
}
function labelForFood(id: string | null) {
  return FOODS.find((f) => f.id === id)?.label ?? "—";
}

export default function SelectedCard({
  item,
  onUpdate,
  onRemove,
}: {
  item: SelectedItem;
  onUpdate: (patch: Partial<SelectedItem>) => void;
  onRemove: () => void;
}) {
  const isComplete = item.times.length > 0 && !!item.food;
  const [editing, setEditing] = useState(!isComplete);

  function toggleTime(id: string) {
    const next = item.times.includes(id)
      ? item.times.filter((t) => t !== id)
      : [...item.times, id];
    onUpdate({ times: next });
  }

  // ─── Compact (collapsed) view ────────────────────────────────
  if (!editing && isComplete) {
    return (
      <div className="bg-white rounded-2xl border border-teal-200 shadow-sm px-4 py-3 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-8 h-8 rounded-full bg-teal-50 flex items-center justify-center flex-shrink-0">
            <Check size={16} className="text-teal-700" />
          </div>
          <div className="min-w-0">
            <div className="text-sm font-bold text-slate-900 truncate">
              {item.drug.generic_en}
            </div>
            <div className="text-xs text-slate-500 truncate">
              {item.times.map(labelForTime).join(", ")} · {labelForFood(item.food)}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-1 flex-shrink-0">
          <button
            onClick={() => setEditing(true)}
            className="p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-700"
            aria-label="Edit"
          >
            <Pencil size={15} />
          </button>
          <button
            onClick={onRemove}
            className="p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-700"
            aria-label="Remove"
          >
            <X size={15} />
          </button>
        </div>
      </div>
    );
  }

  // ─── Expanded (editing) view ─────────────────────────────────
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 px-4 py-3 border-b border-slate-100">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-slate-900">
              {item.drug.generic_en}
            </span>
            {isComplete && (
              <span className="text-[10px] font-bold uppercase text-teal-700 bg-teal-50 px-2 py-0.5 rounded">
                Ready
              </span>
            )}
          </div>
          {item.drug.generic_ar && (
            <div className="text-xs text-slate-500" dir="rtl">
              {item.drug.generic_ar}
            </div>
          )}
        </div>
        <button
          onClick={onRemove}
          className="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition flex-shrink-0"
          aria-label="Remove"
        >
          <X size={16} />
        </button>
      </div>

      {/* Time picker */}
      <div className="px-4 pt-4">
        <div className="text-[11px] font-bold tracking-wider text-slate-500 uppercase mb-2">
          When to take
        </div>
        <div className="grid grid-cols-7 gap-1.5">
          {TIMES.map(({ id, label, Icon }) => {
            const on = item.times.includes(id);
            return (
              <button
                key={id}
                onClick={() => toggleTime(id)}
                className={`flex flex-col items-center gap-1 py-2 rounded-lg border transition ${
                  on
                    ? "border-teal-600 bg-teal-50 text-teal-800"
                    : "border-slate-200 bg-white text-slate-500 hover:border-slate-300 hover:text-slate-700"
                }`}
                title={label}
              >
                <Icon size={18} strokeWidth={on ? 2.2 : 1.8} />
                <span className="text-[10px] leading-none">{label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Food picker */}
      <div className="px-4 py-4">
        <div className="text-[11px] font-bold tracking-wider text-slate-500 uppercase mb-2">
          Relation to food
        </div>
        <div className="grid grid-cols-4 gap-2">
          {FOODS.map(({ id, label, Icon }) => {
            const on = item.food === id;
            return (
              <button
                key={id}
                onClick={() => onUpdate({ food: on ? null : id })}
                className={`flex flex-col items-center gap-1 py-3 rounded-lg border transition ${
                  on
                    ? "border-teal-600 bg-teal-50 text-teal-800"
                    : "border-slate-200 bg-white text-slate-500 hover:border-slate-300 hover:text-slate-700"
                }`}
              >
                <Icon size={20} strokeWidth={on ? 2.2 : 1.8} />
                <span className="text-[10px] leading-tight text-center">{label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Action bar */}
      <div className="px-4 pb-4 flex items-center justify-between gap-3">
        <div className="text-xs text-slate-500">
          {isComplete
            ? "All set — click Done to save."
            : item.times.length === 0
              ? "Pick at least one time."
              : "Pick a food relation."}
        </div>
        <button
          disabled={!isComplete}
          onClick={() => setEditing(false)}
          className="px-4 py-2 rounded-lg bg-teal-700 text-white font-semibold text-sm disabled:bg-slate-300 disabled:cursor-not-allowed transition"
        >
          Done
        </button>
      </div>
    </div>
  );
}