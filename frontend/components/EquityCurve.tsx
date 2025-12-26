'use client';

import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function EquityCurve({
  series,
  title,
}: {
  series: { date: string; value: number }[];
  title: string;
}) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900 p-4">
      <h3 className="mb-4 text-sm font-semibold text-slate-200">{title}</h3>
      <Plot
        data={[
          {
            type: 'scatter',
            mode: 'lines',
            x: series.map((d) => d.date),
            y: series.map((d) => d.value),
            line: { color: '#38bdf8' },
          },
        ]}
        layout={{
          autosize: true,
          height: 300,
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          font: { color: '#e2e8f0' },
          margin: { l: 30, r: 30, t: 10, b: 30 },
        }}
        config={{ displayModeBar: false }}
        style={{ width: '100%' }}
      />
    </div>
  );
}
