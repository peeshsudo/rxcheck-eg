"use client";

export default function MatchList({ matches, onSelect }: any) {
  return (
    <div className="mt-3 space-y-2">
      <p className="text-xs text-[#7C8B85]">اختر الدواء المطابق:</p>
      {matches.map((m: any) => (
        <button
          key={m.id}
          onClick={() => onSelect(m)}
          className="w-full text-start p-3 border rounded-lg hover:bg-[#DCEDE9]"
        >
          <div className="font-bold">{m.brand_ar} — {m.brand_en}</div>
          <div className="text-xs text-[#7C8B85]">{m.form} · {m.strength}</div>
        </button>
      ))}
    </div>
  );
}