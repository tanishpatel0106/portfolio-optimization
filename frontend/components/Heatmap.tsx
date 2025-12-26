export default function Heatmap({
  title,
  rows,
}: {
  title: string;
  rows: { label: string; values: string[] }[];
}) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900 p-4">
      <h3 className="mb-4 text-sm font-semibold text-slate-200">{title}</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full text-xs text-slate-300">
          <tbody>
            {rows.map((row) => (
              <tr key={row.label}>
                <td className="py-1 pr-3 font-medium text-slate-400">
                  {row.label}
                </td>
                {row.values.map((value, index) => (
                  <td
                    key={`${row.label}-${index}`}
                    className="px-2 py-1 text-center"
                  >
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
