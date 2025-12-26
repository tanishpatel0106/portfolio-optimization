export default function PortfolioBuilderPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Portfolio Builder</h2>
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded border border-slate-800 bg-slate-900 p-6 text-sm text-slate-300">
          <h3 className="mb-2 text-sm font-semibold text-slate-200">
            Weights Mode
          </h3>
          <p>Define target weights (long/short) and constraints.</p>
        </div>
        <div className="rounded border border-slate-800 bg-slate-900 p-6 text-sm text-slate-300">
          <h3 className="mb-2 text-sm font-semibold text-slate-200">
            Transactions Mode
          </h3>
          <p>Upload trades, track lots, and preview positions immediately.</p>
        </div>
      </div>
    </div>
  );
}
