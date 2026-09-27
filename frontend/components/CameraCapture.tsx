"use client";
import { useRef, useState } from "react";
import MatchList from "./MatchList";

type Drug = {
  id: string;
  generic_en: string;
  generic_ar: string | null;
  drug_class: string | null;
};

// Common OCR noise words — skipped when guessing drug names
const NOISE = new Set([
  "ref", "lot", "batch", "exp", "mfg", "the", "and", "for", "with",
  "capsule", "capsules", "tablet", "tablets", "suspension", "syrup",
  "each", "contains", "mg", "ml", "gm", "g", "mcg", "iu",
  // Arabic noise
  "الاستعمال", "الجرعة", "كبسولة", "كبسولات", "اقراص", "أقراص",
  "شراب", "انظر", "للنشرة", "الداخلية", "علبة", "تركيز", "مجم",
  "معوي", "معوية", "واسع", "المدى", "مطهر", "علاج", "لعلاج",
]);

function extractCandidates(text: string): string[] {
  const tokens = text
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .split(/\s+/)
    .map((t) => t.trim())
    .filter((t) => t.length >= 3 && !/^\d+$/.test(t))
    .filter((t) => !NOISE.has(t.toLowerCase()));

  // Build single tokens + adjacent pairs (for multi-word names like
  // "حمض الفالبرويك" or "Clavulanic Acid")
  const singles = [...tokens];
  const pairs: string[] = [];
  for (let i = 0; i < tokens.length - 1; i++) {
    pairs.push(`${tokens[i]} ${tokens[i + 1]}`);
  }

  // Longest first — real drug names tend to be longer than noise
  return [...pairs, ...singles].sort((a, b) => b.length - a.length);
}

export default function CameraCapture({ onMatched }: { onMatched: (d: Drug) => void }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [q, setQ] = useState("");
  const [matches, setMatches] = useState<Drug[]>([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  async function apiSearch(query: string): Promise<Drug[]> {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/drugs/search?q=${encodeURIComponent(
      query.trim().slice(0, 40)
    )}`;
    try {
      const res = await fetch(url);
      if (!res.ok) return [];
      const data = await res.json();
      return Array.isArray(data) ? data : [];
    } catch {
      return [];
    }
  }

  async function smartSearch(text: string) {
    const candidates = extractCandidates(text);
    if (candidates.length === 0) {
      setStatusMsg("لم يتم التعرف على نص. اكتب الاسم يدوياً.");
      return;
    }

    setStatusMsg(`جاري البحث في ${candidates.length} كلمة مرشحة...`);

    // Try each candidate longest-first. Stop at first non-empty result.
    for (let i = 0; i < candidates.length; i++) {
      const c = candidates[i];
      setStatusMsg(`محاولة ${i + 1}/${candidates.length}: "${c}"`);
      const results = await apiSearch(c);
      if (results.length > 0) {
        setQ(c);
        setMatches(results);
        setStatusMsg(null);
        return;
      }
    }

    // Nothing matched — fall back to the two longest tokens joined
    setStatusMsg("لم يتم العثور على تطابق. جرّب كلمة من الاسم.");
    setMatches([]);
  }

  async function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setMatches([]);
    setStatusMsg("جاري التعرف على الصورة...");
    setProgress(0);

    try {
      const Tesseract = (await import("tesseract.js")).default;

      const worker = await Tesseract.createWorker(["ara", "eng"], 1, {
        logger: (m: any) => {
          if (m.status === "recognizing text") setProgress(m.progress || 0);
        },
        errorHandler: (err: any) => console.warn("[tesseract]", err),
      });

      const {
        data: { text },
      } = await worker.recognize(file);
      await worker.terminate();
      setProgress(0);

      // Show what OCR extracted so the user can debug
      const cleaned = text.replace(/\s+/g, " ").trim().slice(0, 120);
      console.log("[ocr text]", cleaned);

      await smartSearch(text);
    } catch (err) {
      console.warn("[ocr] failed:", err);
      setProgress(0);
      setStatusMsg("تعذّر قراءة الصورة. اكتب اسم الدواء يدوياً.");
    }
  }

  async function manualSearch() {
    if (q.trim().length < 2) return;
    setLoading(true);
    setStatusMsg(null);
    const results = await apiSearch(q);
    setMatches(results);
    if (results.length === 0) setStatusMsg("لا نتائج. جرّب اسماً آخر.");
    setLoading(false);
  }

  return (
    <div className="bg-white rounded-xl border p-4 space-y-3">
      <button
        className="w-full p-4 rounded-xl border-2 border-dashed border-teal-600 bg-teal-50 text-teal-800 font-bold hover:bg-teal-100 transition"
        onClick={() => inputRef.current?.click()}
      >
        📷 صوّر علبة الدواء
      </button>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFile}
        className="hidden"
      />

      {preview && <img src={preview} alt="معاينة" className="w-full rounded-lg" />}

      {progress > 0 && progress < 1 && (
        <p className="text-xs text-slate-500">
          جاري التعرف... {Math.round(progress * 100)}%
        </p>
      )}

      {statusMsg && <p className="text-xs text-amber-700">{statusMsg}</p>}

      <div className="border-t pt-3">
        <p className="text-xs text-slate-500 mb-2">أو اكتب اسم الدواء:</p>
        <div className="flex gap-2">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && manualSearch()}
            placeholder="aspirin / أسبرين"
            className="flex-1 p-3 border border-slate-200 rounded-lg text-sm focus:border-teal-500 focus:outline-none"
          />
          <button
            onClick={manualSearch}
            disabled={loading || q.trim().length < 2}
            className="px-4 rounded-lg bg-teal-700 text-white font-bold disabled:opacity-40 text-sm"
          >
            {loading ? "..." : "بحث"}
          </button>
        </div>
      </div>

      {matches.length > 0 && <MatchList matches={matches} onSelect={onMatched} />}
    </div>
  );
}