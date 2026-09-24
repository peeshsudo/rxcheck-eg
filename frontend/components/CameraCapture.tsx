"use client";
import { useRef, useState } from "react";
import MatchList from "./MatchList";

type Drug = {
  id: string;
  generic_en: string;
  generic_ar: string | null;
  drug_class: string | null;
};

export default function CameraCapture({ onMatched }: { onMatched: (d: Drug) => void }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [q, setQ] = useState("");
  const [matches, setMatches] = useState<Drug[]>([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  async function search(text: string) {
    const query = text.trim().slice(0, 30);
    if (query.length < 2) return;
    setLoading(true);
    setError(null);
    try {
      const url = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/drugs/search?q=${encodeURIComponent(query)}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const list = Array.isArray(data) ? data : [];
      setMatches(list);
      if (list.length === 0) setError("لا نتائج. جرّب اسماً آخر.");
    } catch (e: any) {
      setError(`تعذّر البحث: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setError(null);
    setProgress(0);

    // ---- Tesseract v5 API ----
    // Dynamic import prevents the crash if the module fails to load
    try {
      const Tesseract = (await import("tesseract.js")).default;

      const worker = await Tesseract.createWorker(["eng", "ara"], 1, {
        logger: (m: any) => {
          if (m.status === "recognizing text") setProgress(m.progress || 0);
        },
        // Silence the "read image" error path
        errorHandler: (err: any) => console.warn("[tesseract]", err),
      });

      const { data: { text } } = await worker.recognize(file);
      await worker.terminate();

      setProgress(0);

      // Take the longest word-looking token
      const tokens = text
        .replace(/[^\w\u0600-\u06FF\s]/g, " ")
        .split(/\s+/)
        .filter((w) => w.length >= 3)
        .slice(0, 4);

      const query = tokens.join(" ").slice(0, 30);
      if (query) {
        setQ(query);
        await search(query);
      } else {
        setError("لم يتم التعرف على نص. اكتب الاسم يدوياً.");
      }
    } catch (err: any) {
      console.warn("[ocr] failed:", err);
      setProgress(0);
      setError("تعذّر قراءة الصورة. اكتب اسم الدواء يدوياً.");
    }
  }

  return (
    <div className="bg-white rounded-xl border p-4 space-y-3">
      <button
        className="w-full p-4 rounded-xl border-2 border-dashed border-[#0F5C56] bg-[#DCEDE9] text-[#0F5C56] font-bold"
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
        <p className="text-xs text-[#7C8B85]">
          جاري التعرف... {Math.round(progress * 100)}%
        </p>
      )}

      <div className="border-t pt-3">
        <p className="text-xs text-[#7C8B85] mb-2">أو اكتب اسم الدواء:</p>
        <div className="flex gap-2">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && search(q)}
            placeholder="aspirin / أسبرين"
            className="flex-1 p-3 border rounded-lg"
          />
          <button
            onClick={() => search(q)}
            disabled={loading || q.trim().length < 2}
            className="px-4 rounded-lg bg-[#0F5C56] text-white font-bold disabled:opacity-40"
          >
            {loading ? "..." : "بحث"}
          </button>
        </div>
      </div>

      {error && <p className="text-xs text-red-600">{error}</p>}
      {matches.length > 0 && <MatchList matches={matches} onSelect={onMatched} />}
    </div>
  );
}