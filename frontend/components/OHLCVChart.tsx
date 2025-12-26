'use client';

import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

interface OHLCVPoint {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export default function OHLCVChart({
  data,
  title,
}: {
  data: OHLCVPoint[];
  title: string;
}) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900 p-4">
      <h3 className="mb-4 text-sm font-semibold text-slate-200">{title}</h3>
      <Plot
        data={[
          {
            type: 'candlestick',
            x: data.map((d) => d.date),
            open: data.map((d) => d.open),
            high: data.map((d) => d.high),
            low: data.map((d) => d.low),
            close: data.map((d) => d.close),
            name: 'Price',
          },
          {
            type: 'bar',
            x: data.map((d) => d.date),
            y: data.map((d) => d.volume),
            name: 'Volume',
            yaxis: 'y2',
            marker: { color: 'rgba(148, 163, 184, 0.4)' },
          },
        ]}
        layout={{
          autosize: true,
          height: 320,
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          font: { color: '#e2e8f0' },
          margin: { l: 30, r: 30, t: 10, b: 30 },
          yaxis: { title: 'Price' },
          yaxis2: {
            title: 'Volume',
            overlaying: 'y',
            side: 'right',
            showgrid: false,
          },
        }}
        config={{ displayModeBar: false }}
        style={{ width: '100%' }}
      />
    </div>
  );
}
