"use client";
import { useState } from "react";
import CameraCapture from "./CameraCapture";
import TimeSelector from "./TimeSelector";
import FoodSelector from "./FoodSelector";

type Drug = {
  id: string;
  generic_en: string;
  generic_ar: string | null;
  drug_class: string | null;
};

function getUserId(): string {
  if (typeof window === "undefined") return "";
  let uid = localStorage.getItem("rxcheck_user_id");
  if (!uid) {
    uid = crypto.randomUUID();
    localStorage.setItem("rxcheck_user_id", uid);
  }
  return uid;
}

export default function ScanFlow() {
  const [step, setStep] = useState(1);
  const [drug, setDrug] = useState<Drug | null>(null);
  const [times, setTimes] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleFood(food: string | null) {
    if (!drug) return;
    setSaving(true);
    setError(null);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/schedules/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: getUserId(),
          product_id: null,
          custom_name: drug.generic_ar || drug.generic_en,
          time_slots: times,
          food_relation: food,
          dose_note: null,
        }),
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`HTTP ${res.status}: ${txt}`);
      }
      setSaved(true);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  }

  function reset() {
    setStep(1);
    setDrug(null);
    setTimes([]);
    setSaved(false);
    setError(null);
  }

  if (saved) {
    return (
      <div className="bg-white rounded-xl border p-6 text-center space-y-3">
        <div className="text-4xl">✅</div>
        <h2 className="font-bold">تم حفظ التذكير</h2>
        <p className="text-sm text-[#7C8B85]">
          {drug?.generic_ar || drug?.generic_en}
        </p>
        <button
          onClick={reset}
          className="px-4 py-2 rounded-lg bg-[#0F5C56] text-white font-bold"
        >
          إضافة تذكير آخر
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 text-xs text-[#7C8B85]">
        <span className={step === 1 ? "text-[#0F5C56] font-bold" : ""}>١. الدواء</span>
        <span>›</span>
        <span className={step === 2 ? "text-[#0F5C56] font-bold" : ""}>٢. الأوقات</span>
        <span>›</span>
        <span className={step === 3 ? "text-[#0F5C56] font-bold" : ""}>٣. الطعام</span>
      </div>

      {step === 1 && (
        <CameraCapture onMatched={(d) => { setDrug(d); setStep(2); }} />
      )}
      {step === 2 && drug && (
        <TimeSelector drug={drug} onNext={(t: string[]) => { setTimes(t); setStep(3); }} />
      )}
      {step === 3 && drug && (
        <FoodSelector drug={drug} times={times} onSubmit={handleFood} />
      )}

      {error && <p className="text-xs text-red-600">{error}</p>}
      {saving && <p className="text-xs text-[#7C8B85]">جاري الحفظ...</p>}

      {step > 1 && !saving && (
        <button
          onClick={() => setStep(step - 1)}
          className="text-xs text-[#7C8B85] underline"
        >
          ← رجوع
        </button>
      )}
    </div>
  );
}