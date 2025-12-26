export function ExposureBreakdown({
  title,
  items
}: {
  title: string;
  items: { label: string; value: string }[];
}) {
  return (
    <div className="rounded border border-slate-200 bg-white p-4">
      <h3 className="text-sm font-semibold text-slate-700">{title}</h3>
      <ul className="mt-4 space-y-2 text-sm">
        {items.map((item) => (
          <li key={item.label} className="flex justify-between">
            <span className="text-slate-500">{item.label}</span>
            <span className="font-medium text-slate-900">{item.value}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
