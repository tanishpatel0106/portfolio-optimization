import MetricsTable from '../../components/MetricsTable';

export default function TailStressPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Tail & Stress</h2>
      <MetricsTable
        title="VaR / CVaR"
        metrics={[
          { label: 'Hist VaR 95%', value: '-2.3%' },
          { label: 'Hist CVaR 95%', value: '-3.1%' },
          { label: 'Param VaR 95%', value: '-2.0%' },
          { label: 'Param CVaR 95%', value: '-2.8%' },
        ]}
      />
    </div>
  );
}
