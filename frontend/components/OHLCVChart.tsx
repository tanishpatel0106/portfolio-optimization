"use client";

import Plot from "./Plotly";

type OHLCVPoint = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export function OHLCVChart({ data, title }: { data: OHLCVPoint[]; title: string }) {
  return (
    <Plot
      data={[
        {
          type: "candlestick",
          x: data.map((d) => d.date),
          open: data.map((d) => d.open),
          high: data.map((d) => d.high),
          low: data.map((d) => d.low),
          close: data.map((d) => d.close),
          name: "Price"
        },
        {
          type: "bar",
          x: data.map((d) => d.date),
          y: data.map((d) => d.volume),
          name: "Volume",
          yaxis: "y2",
          marker: { color: "rgba(100,116,139,0.4)" }
        }
      ]}
      layout={{
        title,
        height: 420,
        margin: { l: 50, r: 50, t: 50, b: 40 },
        yaxis: { title: "Price" },
        yaxis2: { title: "Volume", overlaying: "y", side: "right", showgrid: false }
      }}
      config={{ displayModeBar: false, responsive: true }}
    />
  );
}
