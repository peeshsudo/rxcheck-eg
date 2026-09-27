"use client";
import { useEffect, useRef, useState } from "react";
import { Search, Loader2 } from "lucide-react";

type Drug = {
  id: string;
  generic_en: string;
  generic_ar: string | null;
  drug_class: string | null;
};

export default function SearchCombobox({
  kind,
  placeholder,
  onPick,
  excludeIds = [],
}: {
  kind: "medicine" | "food";
  placeholder: string;
  onPick: (d: Drug) => void;
  excludeIds?: string[];
}) {
  const [q, setQ] = useState("");
  const [results, setResults] = useState<Drug[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const boxRef = useRef<HTMLDivElement>(null);

  // Debounced search
  useEffect(() => {
    if (kind === "food") {
      setResults([]);
      return;
    }
    const t = setTimeout(async () => {
      if (q.trim().length < 2) {
        setResults([]);
        return;
      }
      setLoading(true);
      try {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/drugs/search?q=${encodeURIComponent(q.trim())}`;
        const r = await fetch(url);
        if (r.ok) {
          const data = await r.json();
          setResults(
            (Array.isArray(data) ? data : []).filter((d) => !excludeIds.includes(d.id))
          );
        } else {
          setResults([]);
        }
      } catch {
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [q, kind, excludeIds]);

  // Close on outside click
  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  function pick(d: Drug) {
    onPick(d);
    setQ("");
    setResults([]);
    setOpen(false);
  }

  return (
    <div ref={boxRef} className="relative">
      <div className="relative">
        <Search
          size={18}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
        />
        <input
          value={q}
          onChange={(e) => {
            setQ(e.target.value);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
          placeholder={placeholder}
          className="w-full pl-10 pr-10 py-3 rounded-xl bg-slate-100 border border-slate-200 text-sm text-slate-800 placeholder:text-slate-400 focus:bg-white focus:border-teal-500 focus:ring-1 focus:ring-teal-500 focus:outline-none transition"
        />
        {loading && (
          <Loader2
            size={16}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 animate-spin"
          />
        )}
      </div>

      {open && results.length > 0 && (
        <div className="absolute z-30 mt-1 w-full bg-white border border-slate-200 rounded-xl shadow-lg max-h-72 overflow-y-auto">
          {results.map((d) => (
            <button
              key={d.id}
              onClick={() => pick(d)}
              className="w-full text-left px-4 py-3 hover:bg-teal-50 border-b border-slate-100 last:border-none transition"
            >
              <div className="flex items-center justify-between gap-2">
                <div>
                  <div className="text-sm font-semibold text-slate-900">
                    {d.generic_en}
                  </div>
                  {d.generic_ar && (
                    <div className="text-xs text-slate-500" dir="rtl">
                      {d.generic_ar}
                    </div>
                  )}
                </div>
                {d.drug_class && (
                  <span className="text-[10px] uppercase font-semibold text-teal-700 bg-teal-50 px-2 py-0.5 rounded">
                    {d.drug_class}
                  </span>
                )}
              </div>
            </button>
          ))}
        </div>
      )}

      {open && !loading && q.trim().length >= 2 && results.length === 0 && kind === "medicine" && (
        <div className="absolute z-30 mt-1 w-full bg-white border border-slate-200 rounded-xl shadow-lg px-4 py-3 text-xs text-slate-400">
          No matches. Try a different spelling.
        </div>
      )}
    </div>
  );
}