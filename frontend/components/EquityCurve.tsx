"use client";

import Plot from "./Plotly";

export function EquityCurve({ series }: { series: { date: string; value: number }[] }) {
  return (
    <Plot
      data={[
        {
          type: "scatter",
          mode: "lines",
          x: series.map((d) => d.date),
          y: series.map((d) => d.value),
          line: { color: "#0f172a" }
        }
      ]}
      layout={{ height: 320, margin: { l: 40, r: 20, t: 40, b: 40 }, title: "Equity Curve" }}
      config={{ displayModeBar: false, responsive: true }}
    />
  );
}
