"use client";
import { useState } from "react";
import CameraCapture from "./CameraCapture";
import TimeSelector from "./TimeSelector";
import FoodSelector from "./FoodSelector";
import InteractionPanel from "./InteractionPanel";

type Drug = {
  id: string;
  generic_en: string;
  generic_ar: string | null;
  drug_class: string | null;
};

type SavedMed = {
  id: string;
  name: string;
  genericEn: string;
  times: string[];
  food: string | null;
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
  const [savedMeds, setSavedMeds] = useState<SavedMed[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function handleFood(food: string | null) {
    if (!drug) return;

    // Duplicate check
    const existing = savedMeds.find(
      (m) =>
        m.name.trim() === (drug.generic_ar || drug.generic_en).trim() ||
        m.genericEn === drug.generic_en
    );

    if (existing) {
      const replace = window.confirm(
        `⚠️ هذا الدواء موجود في القائمة بالفعل:\n\n` +
          `${existing.name}\n` +
          `🕐 ${existing.times.join(", ")} | 🍽️ ${existing.food || "—"}\n\n` +
          `هل تريد استبداله بالإدخال الجديد؟\n` +
          `(موافق = استبدال، إلغاء = الاحتفاظ بالقديم)`
      );
      if (!replace) {
        setDrug(null);
        setTimes([]);
        setStep(1);
        return;
      }
      setSavedMeds((prev) => prev.filter((m) => m.id !== existing.id));
    }

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
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);

      setSavedMeds((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          name: drug.generic_ar || drug.generic_en,
          genericEn: drug.generic_en,
          times,
          food,
        },
      ]);

      setDrug(null);
      setTimes([]);
      setStep(1);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Step indicators */}
      <div className="flex items-center gap-2 text-xs text-[#7C8B85]">
        <span className={step === 1 ? "text-[#0F5C56] font-bold" : ""}>١. الدواء</span>
        <span>›</span>
        <span className={step === 2 ? "text-[#0F5C56] font-bold" : ""}>٢. الأوقات</span>
        <span>›</span>
        <span className={step === 3 ? "text-[#0F5C56] font-bold" : ""}>٣. الطعام</span>
      </div>

      {step === 1 && (
        <CameraCapture
          onMatched={(d) => {
            setDrug(d);
            setStep(2);
          }}
        />
      )}

      {step === 2 && drug && (
        <TimeSelector
          drug={drug}
          onNext={(t: string[]) => {
            setTimes(t);
            setStep(3);
          }}
        />
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

      {savedMeds.length > 0 && (
        <section className="bg-white rounded-xl border p-4 space-y-3">
          <h2 className="font-bold">قائمة الأدوية ({savedMeds.length})</h2>
          <ul className="space-y-2">
            {savedMeds.map((m) => (
              <li
                key={m.id}
                className="p-3 border rounded-lg flex justify-between items-start"
              >
                <div>
                  <div className="font-bold text-sm">{m.name}</div>
                  <div className="text-xs text-[#7C8B85]">
                    🕐 {m.times.join(", ")} · 🍽️ {m.food || "—"}
                  </div>
                </div>
                <button
                  onClick={() => setSavedMeds((prev) => prev.filter((x) => x.id !== m.id))}
                  className="text-xs text-red-600 hover:underline"
                >
                  حذف
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      {savedMeds.length >= 2 && <InteractionPanel meds={savedMeds} />}
    </div>
  );
}