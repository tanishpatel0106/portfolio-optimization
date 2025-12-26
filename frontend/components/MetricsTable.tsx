export function MetricsTable({ metrics }: { metrics: { label: string; value: string }[] }) {
  return (
    <div className="rounded border border-slate-200 bg-white p-4">
      <h3 className="text-sm font-semibold text-slate-700">Key Metrics</h3>
      <dl className="mt-4 space-y-2 text-sm">
        {metrics.map((metric) => (
          <div key={metric.label} className="flex justify-between">
            <dt className="text-slate-500">{metric.label}</dt>
            <dd className="font-medium text-slate-900">{metric.value}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
