import ScanFlow from "@/components/ScanFlow";

export default function Home() {
  return (
    <main className="max-w-md mx-auto p-4">
      <header className="mb-4">
        <h1 className="text-xl font-bold">RxCheck EG</h1>
        <p className="text-sm text-[#7C8B85]">امسح علبة الدواء لتحديده</p>
      </header>
      <ScanFlow />
    </main>
  );
}