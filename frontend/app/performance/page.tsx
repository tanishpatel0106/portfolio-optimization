import { EquityCurve } from "../../components/EquityCurve";
import { MetricsTable } from "../../components/MetricsTable";

const series = [
  { date: "2024-05-01", value: 100 },
  { date: "2024-05-15", value: 104 },
  { date: "2024-06-01", value: 110 }
];

export default function PerformancePage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Performance Dashboard</h2>
      <div className="grid gap-4 md:grid-cols-2">
        <MetricsTable
          metrics={[
            { label: "Cumulative Return", value: "+10.2%" },
            { label: "CAGR", value: "9.1%" },
            { label: "Annual Vol", value: "12.4%" }
          ]}
        />
        <MetricsTable
          metrics={[
            { label: "Sharpe", value: "1.18" },
            { label: "Sortino", value: "1.52" },
            { label: "Calmar", value: "0.84" }
          ]}
        />
      </div>
      <EquityCurve series={series} />
    </div>
  );
}
