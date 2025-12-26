export default function MetricsTable({
  title,
  metrics,
}: {
  title: string;
  metrics: { label: string; value: string }[];
}) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900 p-4">
      <h3 className="mb-4 text-sm font-semibold text-slate-200">{title}</h3>
      <div className="space-y-2 text-sm">
        {metrics.map((metric) => (
          <div key={metric.label} className="flex justify-between text-slate-300">
            <span>{metric.label}</span>
            <span className="font-medium text-slate-100">{metric.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
