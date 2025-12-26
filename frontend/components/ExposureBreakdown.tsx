export default function ExposureBreakdown({
  title,
  items,
}: {
  title: string;
  items: { label: string; value: string }[];
}) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900 p-4">
      <h3 className="mb-4 text-sm font-semibold text-slate-200">{title}</h3>
      <ul className="space-y-2 text-sm text-slate-300">
        {items.map((item) => (
          <li key={item.label} className="flex justify-between">
            <span>{item.label}</span>
            <span className="font-medium text-slate-100">{item.value}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
