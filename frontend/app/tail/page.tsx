import { MetricsTable } from "../../components/MetricsTable";

export default function TailPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Tail & Stress</h2>
      <MetricsTable
        metrics={[
          { label: "Hist VaR (95%)", value: "-2.4%" },
          { label: "Hist CVaR", value: "-3.6%" },
          { label: "Worst 1M", value: "-8.9%" }
        ]}
      />
      <div className="rounded border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-500">
        Stress scenario sliders placeholder.
      </div>
    </div>
  );
}
