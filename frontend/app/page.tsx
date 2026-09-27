"use client";
import { useState } from "react";
import TabBar, { TabId } from "@/components/TabBar";
import CheckPanel from "@/components/CheckPanel";
import AssistantPanel from "@/components/AssistantPanel";
import CataloguePanel from "@/components/CataloguePanel";
import CurationPanel from "@/components/CurationPanel";
import AuditPanel from "@/components/AuditPanel";

export default function Home() {
  const [tab, setTab] = useState<TabId>("check");

  return (
    <div className="min-h-screen bg-slate-50 pb-24">
      {tab === "check"     && <CheckPanel />}
      {tab === "assistant" && <AssistantPanel />}
      {tab === "catalogue" && <CataloguePanel />}
      {tab === "curation"  && <CurationPanel />}
      {tab === "audit"     && <AuditPanel />}

      <TabBar active={tab} onChange={setTab} />
    </div>
  );
}