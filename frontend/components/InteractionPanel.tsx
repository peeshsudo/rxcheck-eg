"use client";
import { useState } from "react";

type Med = { id: string; name: string; genericEn: string };

type Interaction = {
  severity: string;
  effect_en: string;
  effect_ar?: string | null;
  management_en?: string | null;
  management_ar?: string | null;
  source: string;
};

const SEV_STYLE: Record<string, string> = {
  severe:   "bg-red-50 border-red-300 text-red-900",
  moderate: "bg-amber-50 border-amber-300 text-amber-900",
  mild:     "bg-yellow-50 border-yellow-300 text-yellow-900",
  unknown:  "bg-slate-50 border-slate-300 text-slate-800",
};

export default function InteractionPanel({ meds }: { meds: Med[] }) {
  const [loading, setLoading] = useState(false);
  const [checked, setChecked] = useState(false);
  const [results, setResults] = useState<Interaction[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function check() {
    setLoading(true);
    setError(null);
    try {
      // Look up drug UUIDs by generic name
      const ids: string[] = [];
      for (const m of meds) {
        const r = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/drugs/search?q=${encodeURIComponent(m.genericEn)}`
        );
        if (!r.ok) continue;
        const list = await r.json();
        if (list[0]?.id) ids.push(list[0].id);
      }

      if (ids.length < 2) {
        setError("تعذّر العثور على معرّفات الأدوية.");
        setResults([]);
        setChecked(true);
        return;
      }

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/interactions/check-batch`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(ids),
        }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setResults(await res.json());
      setChecked(true);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="bg-white rounded-xl border p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="font-bold">فحص التفاعلات الدوائية</h2>
        <button
          onClick={check}
          disabled={loading}
          className="px-4 py-2 rounded-lg bg-[#0F5C56] text-white font-bold text-sm disabled:opacity-40"
        >
          {loading ? "..." : "افحص"}
        </button>
      </div>

      {error && <p className="text-xs text-red-600">{error}</p>}

      {checked && !loading && results.length === 0 && !error && (
        <p className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg p-3">
          ✅ لا توجد تفاعلات مسجّلة بين الأدوية المختارة. هذا لا يعني أنها آمنة تماماً — استشر الصيدلي.
        </p>
      )}

      {results.map((r, i) => (
        <div
          key={i}
          className={`p-3 rounded-lg border ${SEV_STYLE[r.severity] || SEV_STYLE.unknown}`}
        >
          <div className="text-xs font-bold uppercase mb-1">
            {r.severity}
          </div>
          <p className="text-sm">{r.effect_ar || r.effect_en}</p>
          {(r.management_ar || r.management_en) && (
            <p className="text-xs mt-1 opacity-80">
              💡 {r.management_ar || r.management_en}
            </p>
          )}
          <p className="text-[10px] mt-1 opacity-60">المصدر: {r.source}</p>
        </div>
      ))}
    </section>
  );
}