export default function UniverseBuilderPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Universe Builder</h2>
      <div className="rounded border border-slate-800 bg-slate-900 p-6 text-sm text-slate-300">
        <p className="mb-2">
          Manage instruments, metadata, and CSV imports for the global investable universe.
        </p>
        <ul className="list-disc space-y-1 pl-5">
          <li>Validate missing currency, region, or asset class metadata.</li>
          <li>Import/export CSV templates for bulk updates.</li>
          <li>Tag instruments by sector, style, or duration bucket.</li>
        </ul>
      </div>
    </div>
  );
}
