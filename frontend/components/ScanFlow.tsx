"use client";
import { useState } from "react";
import CameraCapture from "./CameraCapture";
import MatchList from "./MatchList";
import TimeSelector from "./TimeSelector";
import FoodSelector from "./FoodSelector";

export default function ScanFlow() {
  const [step, setStep] = useState(1);
  const [matchedDrug, setMatchedDrug] = useState<any>(null);
  const [times, setTimes] = useState<string[]>([]);
  const [food, setFood] = useState<string | null>(null);

  return (
    <div className="space-y-4">
      {step === 1 && (
        <CameraCapture
          onMatched={(drug) => { setMatchedDrug(drug); setStep(2); }}
        />
      )}
      {step === 2 && matchedDrug && (
        <TimeSelector
          drug={matchedDrug}
          onNext={(t) => { setTimes(t); setStep(3); }}
        />
      )}
      {step === 3 && (
        <FoodSelector
          drug={matchedDrug}
          times={times}
          onSubmit={(f) => save({ drug: matchedDrug, times, food: f })}
        />
      )}
    </div>
  );
}

async function save(schedule: any) {
  await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/schedules/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: crypto.randomUUID(),
      product_id: schedule.drug?.productId,
      custom_name: schedule.drug?.brandAr,
      time_slots: schedule.times,
      food_relation: schedule.food,
    }),
  });
  alert("✅ تم حفظ التذكير");
}