import { OHLCVChart } from "../../components/OHLCVChart";

const sample = [
  { date: "2024-06-01", open: 180, high: 184, low: 178, close: 182, volume: 15000 },
  { date: "2024-06-02", open: 182, high: 185, low: 181, close: 183, volume: 14800 },
  { date: "2024-06-03", open: 183, high: 187, low: 182, close: 186, volume: 15500 }
];

export default function AssetExplorerPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Asset Explorer</h2>
      <p className="text-sm text-slate-600">Candlestick view with trade and position markers.</p>
      <OHLCVChart data={sample} title="AAPL OHLCV" />
    </div>
  );
}
