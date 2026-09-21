"use client";

type Drug = {
  id: string;
  generic_en: string;
  generic_ar: string | null;
  drug_class: string | null;
};

export default function MatchList({
  matches,
  onSelect,
}: {
  matches: Drug[];
  onSelect: (d: Drug) => void;
}) {
  return (
    <div className="mt-3 space-y-2">
      <p className="text-xs text-[#7C8B85]">اختر الدواء:</p>
      {matches.map((m) => (
        <button
          key={m.id}
          onClick={() => onSelect(m)}
          className="w-full text-start p-3 border rounded-lg hover:bg-[#DCEDE9]"
        >
          <div className="font-bold">
            {m.generic_ar || m.generic_en}
            {m.generic_ar && (
              <span className="text-xs text-[#7C8B85]"> — {m.generic_en}</span>
            )}
          </div>
          {m.drug_class && (
            <div className="text-xs text-[#7C8B85]">{m.drug_class}</div>
          )}
        </button>
      ))}
    </div>
  );
}