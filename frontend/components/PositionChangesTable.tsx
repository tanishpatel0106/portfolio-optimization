export function PositionChangesTable({
  rows
}: {
  rows: { date: string; ticker: string; action: string; delta: string }[];
}) {
  return (
    <div className="rounded border border-slate-200 bg-white p-4">
      <h3 className="text-sm font-semibold text-slate-700">Position Changes</h3>
      <table className="mt-4 w-full text-sm">
        <thead className="text-left text-slate-500">
          <tr>
            <th>Date</th>
            <th>Ticker</th>
            <th>Action</th>
            <th>ΔQty</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={`${row.date}-${row.ticker}`} className="border-t border-slate-100">
              <td className="py-2">{row.date}</td>
              <td className="py-2">{row.ticker}</td>
              <td className="py-2">{row.action}</td>
              <td className="py-2">{row.delta}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
