"use client";
import { useRef, useState } from "react";
import Tesseract from "tesseract.js";

export default function CameraCapture({ onMatched }: { onMatched: (d: any) => void }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [matches, setMatches] = useState<any[]>([]);

  async function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    const { data: { text } } = await Tesseract.recognize(file, "ara+eng", {
      logger: (m) => { if (m.status === "recognizing text") setProgress(m.progress); },
    });
    const results = await fuzzySearch(text);
    setMatches(results);
  }

  return (
    <div className="bg-white rounded-xl border p-4">
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
      {preview && <img src={preview} alt="معاينة" className="w-full mt-3 rounded-lg" />}
      {progress > 0 && progress < 1 && (
        <p className="text-xs text-[#7C8B85] mt-2">جاري التعرف... {Math.round(progress * 100)}%</p>
      )}
      {matches.length > 0 && <MatchList matches={matches} onSelect={onMatched} />}
    </div>
  );
}

async function fuzzySearch(text: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/products/search?q=${encodeURIComponent(text.slice(0, 20))}`
  );
  return res.ok ? await res.json() : [];
}