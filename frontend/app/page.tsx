import OHLCVChart from '../components/OHLCVChart';
import MetricsTable from '../components/MetricsTable';
import HealthBadge from '../components/HealthBadge';
import { sampleOhlcv } from '../lib/sampleData';

const summaryMetrics = [
  { label: 'Base Currency', value: 'USD (62%)' },
  { label: 'Gross Exposure', value: '1.45x' },
  { label: 'Net Exposure', value: '0.92x' },
  { label: 'Last Refresh', value: '2024-05-15' },
];

export default function OverviewPage() {
  return (
    <div className="space-y-6">
      <section className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Overview</h2>
        <HealthBadge />
      </section>
      <section className="grid gap-4 md:grid-cols-4">
        {summaryMetrics.map((metric) => (
          <div
            key={metric.label}
            className="rounded border border-slate-800 bg-slate-900 p-4"
          >
            <p className="text-xs uppercase text-slate-500">{metric.label}</p>
            <p className="mt-2 text-lg font-semibold text-slate-100">{metric.value}</p>
          </div>
        ))}
      </section>
      <section className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <OHLCVChart data={sampleOhlcv} title="Portfolio OHLCV (Base Currency)" />
        </div>
        <MetricsTable
          title="Quick Stats"
          metrics={[
            { label: 'CAGR', value: '12.4%' },
            { label: 'Volatility', value: '9.8%' },
            { label: 'Sharpe', value: '1.1' },
            { label: 'Max Drawdown', value: '-8.2%' },
          ]}
        />
      </section>
    </div>
  );
}
