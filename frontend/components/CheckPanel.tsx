"use client";
import { useState } from "react";
import { ShieldAlert, Camera, X } from "lucide-react";
import SearchCombobox from "./SearchCombobox";
import SelectedCard from "./SelectedCard";
import InteractionPanel from "./InteractionPanel";
import CameraCapture from "./CameraCapture";

type Drug = {
  id: string;
  generic_en: string;
  generic_ar: string | null;
  drug_class: string | null;
  brand_en?: string | null;
  brand_ar?: string | null;
};

export type SelectedItem = {
  uid: string;
  drug: Drug;
  times: string[];
  food: string | null;
};

function newUid() {
  return typeof crypto !== "undefined" ? crypto.randomUUID() : Math.random().toString(36);
}

export default function CheckPanel() {
  const [items, setItems] = useState<SelectedItem[]>([]);
  const [showOcr, setShowOcr] = useState(false);

  function addDrug(d: Drug) {
    setItems((prev) => {
      // Avoid duplicates
      if (prev.some((p) => p.drug.id === d.id)) return prev;
      return [...prev, { uid: newUid(), drug: d, times: [], food: null }];
    });
    setShowOcr(false);
  }

  function update(uid: string, patch: Partial<SelectedItem>) {
    setItems((prev) =>
      prev.map((it) => (it.uid === uid ? { ...it, ...patch } : it))
    );
  }

  function remove(uid: string) {
    setItems((prev) => prev.filter((it) => it.uid !== uid));
  }

  const ready = items.filter((i) => i.times.length > 0 && i.food);
  const canCheck = ready.length >= 2;

  return (
    <div className="pb-12">
      {/* Demo banner */}
      <div className="bg-amber-50 border-b border-amber-200 text-amber-900 text-xs px-4 py-3 leading-relaxed">
        <strong>Demo dataset</strong> — sample data for illustration only. Not
        verified for clinical use; every record needs pharmacist sign-off before
        any real deployment.
      </div>

      <div className="max-w-3xl mx-auto px-4 pt-6">
        <h1 className="text-2xl font-bold text-slate-900">Check interactions</h1>
        <p className="text-sm text-slate-600 mt-1 leading-relaxed">
          Search medicines and foods/supplements, then see what the curated
          dataset knows about how they interact.
        </p>

        {/* OCR button — opens modal */}
        <section className="mt-5">
          <button
            onClick={() => setShowOcr(true)}
            className="w-full flex items-center justify-center gap-2 py-3 rounded-xl border-2 border-dashed border-teal-600 bg-teal-50 text-teal-800 font-semibold text-sm hover:bg-teal-100 transition"
          >
            <Camera size={18} />
            Scan medicine box (OCR)
          </button>
        </section>

        {/* Medicines */}
        <section className="mt-6">
          <label className="block text-xs font-bold tracking-wider text-slate-500 uppercase mb-2">
            Medicines
          </label>
          <SearchCombobox
            kind="medicine"
            placeholder="Search a medicine, e.g. Plavix or clopidogrel"
            onPick={addDrug}
            excludeIds={items.map((i) => i.drug.id)}
          />
        </section>

        {/* Foods — placeholder */}
        <section className="mt-6">
          <label className="block text-xs font-bold tracking-wider text-slate-500 uppercase mb-2">
            Food &amp; supplements
          </label>
          <SearchCombobox
            kind="food"
            placeholder="Search a food or supplement, e.g. grapefruit (coming soon)"
            onPick={() => {}}
            excludeIds={[]}
          />
        </section>

        {items.length === 0 && (
          <p className="text-sm text-slate-400 mt-8">
            Nothing selected yet — search above to add medicines or foods.
          </p>
        )}

        {items.length > 0 && (
          <div className="mt-8 space-y-3">
            {items.map((it) => (
              <SelectedCard
                key={it.uid}
                item={it}
                onUpdate={(patch) => update(it.uid, patch)}
                onRemove={() => remove(it.uid)}
              />
            ))}
          </div>
        )}

        {/* Interaction check block */}
        {items.length >= 2 && (
          <div className="mt-8">
            {canCheck ? (
              <InteractionPanel
                meds={ready.map((i) => ({
                  id: i.drug.id,
                  name: i.drug.generic_ar || i.drug.generic_en,
                  genericEn: i.drug.generic_en,
                }))}
              />
            ) : (
              <div className="bg-white rounded-2xl border border-slate-200 p-5">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <h3 className="font-bold text-slate-900">Check interactions</h3>
                    <p className="text-xs text-slate-500 mt-1">
                      Pick a time and food relation for at least two medicines, then click below.
                    </p>
                  </div>
                  <button
                    disabled
                    className="px-4 py-2 rounded-lg bg-slate-300 text-white font-semibold text-sm cursor-not-allowed"
                  >
                    Check
                  </button>
                </div>
                <div className="mt-3 flex items-center gap-2 text-xs text-amber-700">
                  <ShieldAlert size={14} />
                  <span>
                    {ready.length} of {items.length} medicines ready ({items.length - ready.length} incomplete)
                  </span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* OCR modal */}
      {showOcr && (
        <div
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          onClick={() => setShowOcr(false)}
        >
          <div
            className="bg-white rounded-2xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100">
              <h2 className="font-bold text-slate-900">Scan medicine box</h2>
              <button
                onClick={() => setShowOcr(false)}
                className="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-700"
              >
                <X size={18} />
              </button>
            </div>
            <div className="p-4">
              <CameraCapture onMatched={addDrug} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}