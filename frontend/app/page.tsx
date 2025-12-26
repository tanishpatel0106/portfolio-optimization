import { EquityCurve } from "../components/EquityCurve";
import { MetricsTable } from "../components/MetricsTable";
import { OHLCVChart } from "../components/OHLCVChart";

const ohlcvData = [
  { date: "2024-06-01", open: 100, high: 105, low: 98, close: 103, volume: 12000 },
  { date: "2024-06-02", open: 103, high: 106, low: 101, close: 104, volume: 11000 },
  { date: "2024-06-03", open: 104, high: 108, low: 102, close: 107, volume: 13000 }
];

const equityCurve = [
  { date: "2024-06-01", value: 100 },
  { date: "2024-06-02", value: 102 },
  { date: "2024-06-03", value: 105 }
];

export default function OverviewPage() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <MetricsTable
          metrics={[
            { label: "Base Currency", value: "USD (62%)" },
            { label: "Gross Exposure", value: "1.35" },
            { label: "Net Exposure", value: "0.75" }
          ]}
        />
        <MetricsTable
          metrics={[
            { label: "Top Position", value: "AAPL 18%" },
            { label: "Last Refresh", value: "2024-06-03" },
            { label: "Regime", value: "Risk-On" }
          ]}
        />
        <MetricsTable
          metrics={[
            { label: "Sharpe", value: "1.12" },
            { label: "Max Drawdown", value: "-8.4%" },
            { label: "CAGR", value: "9.6%" }
          ]}
        />
      </div>
      <OHLCVChart data={ohlcvData} title="Portfolio OHLCV" />
      <EquityCurve series={equityCurve} />
    </div>
  );
}
