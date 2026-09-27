"use client";
import { CheckCircle2, MessageCircle, AlignLeft, CheckSquare, Clock } from "lucide-react";

export type TabId = "check" | "assistant" | "catalogue" | "curation" | "audit";

const TABS: { id: TabId; label: string; icon: React.ElementType }[] = [
  { id: "check",     label: "Check",      icon: CheckCircle2 },
  { id: "assistant", label: "Assistant",  icon: MessageCircle },
  { id: "catalogue", label: "Catalogue",  icon: AlignLeft },
  { id: "curation",  label: "Curation",   icon: CheckSquare },
  { id: "audit",     label: "Audit log",  icon: Clock },
];

export default function TabBar({
  active,
  onChange,
}: {
  active: TabId;
  onChange: (id: TabId) => void;
}) {
  return (
    <nav className="fixed bottom-0 inset-x-0 bg-white border-t border-slate-200 z-40">
      <ul className="max-w-3xl mx-auto grid grid-cols-5">
        {TABS.map(({ id, label, icon: Icon }) => {
          const isActive = active === id;
          return (
            <li key={id}>
              <button
                onClick={() => onChange(id)}
                className={`w-full py-3 flex flex-col items-center gap-1 transition-colors ${
                  isActive ? "text-teal-700" : "text-slate-400 hover:text-slate-600"
                }`}
              >
                <Icon size={22} strokeWidth={isActive ? 2.2 : 1.8} />
                <span className={`text-[11px] ${isActive ? "font-semibold" : ""}`}>
                  {label}
                </span>
              </button>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}