export default function PortfolioBuilderPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Portfolio Builder</h2>
      <p className="text-sm text-slate-600">
        Create portfolios, edit weights or trades, and preview current positions.
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-500">
          Weights editor placeholder.
        </div>
        <div className="rounded border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-500">
          Trades blotter placeholder.
        </div>
      </div>
    </div>
  );
}
