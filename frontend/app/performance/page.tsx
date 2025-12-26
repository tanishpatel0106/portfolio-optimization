import EquityCurve from '../../components/EquityCurve';
import Heatmap from '../../components/Heatmap';
import { sampleEquity } from '../../lib/sampleData';

export default function PerformancePage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Performance Dashboard</h2>
      <EquityCurve title="Equity Curve vs Benchmark" series={sampleEquity} />
      <Heatmap
        title="Monthly Returns"
        rows={[
          { label: '2024', values: ['2.1%', '-0.8%', '1.4%', '3.2%'] },
        ]}
      />
    </div>
  );
}
