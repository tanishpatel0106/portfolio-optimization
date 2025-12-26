import Heatmap from '../../components/Heatmap';
import MetricsTable from '../../components/MetricsTable';

export default function RiskLabPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Risk Lab</h2>
      <div className="grid gap-4 lg:grid-cols-2">
        <Heatmap
          title="Correlation Matrix"
          rows={[
            { label: 'Portfolio', values: ['1.00', '0.62', '0.41'] },
            { label: 'Benchmark', values: ['0.62', '1.00', '0.33'] },
            { label: 'Hedge', values: ['0.41', '0.33', '1.00'] },
          ]}
        />
        <MetricsTable
          title="Tracking Metrics"
          metrics={[
            { label: 'Beta', value: '0.87' },
            { label: 'Tracking Error', value: '4.2%' },
            { label: 'Information Ratio', value: '0.45' },
          ]}
        />
      </div>
    </div>
  );
}
