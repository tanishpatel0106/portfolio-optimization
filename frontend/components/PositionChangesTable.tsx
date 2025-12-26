export default function PositionChangesTable({
  rows,
}: {
  rows: { date: string; ticker: string; action: string; delta: string }[];
}) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900 p-4">
      <h3 className="mb-4 text-sm font-semibold text-slate-200">Position Changes</h3>
      <table className="w-full text-left text-sm text-slate-300">
        <thead className="text-xs uppercase text-slate-500">
          <tr>
            <th className="py-2">Date</th>
            <th>Ticker</th>
            <th>Action</th>
            <th className="text-right">Δ Qty</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.ticker}-${index}`} className="border-t border-slate-800">
              <td className="py-2">{row.date}</td>
              <td>{row.ticker}</td>
              <td>{row.action}</td>
              <td className="text-right">{row.delta}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
