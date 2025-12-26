import { Heatmap } from "../../components/Heatmap";

export default function RiskPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Risk Lab</h2>
      <Heatmap
        title="Correlation Heatmap"
        xLabels={["AAPL", "SPY", "EWJ"]}
        yLabels={["AAPL", "SPY", "EWJ"]}
        values={[
          [1, 0.8, 0.6],
          [0.8, 1, 0.55],
          [0.6, 0.55, 1]
        ]}
      />
    </div>
  );
}
