"use client";

import Plot from "./Plotly";

export function Heatmap({
  xLabels,
  yLabels,
  values,
  title
}: {
  xLabels: string[];
  yLabels: string[];
  values: number[][];
  title: string;
}) {
  return (
    <Plot
      data={[
        {
          type: "heatmap",
          x: xLabels,
          y: yLabels,
          z: values,
          colorscale: "Viridis"
        }
      ]}
      layout={{ height: 320, margin: { l: 40, r: 20, t: 40, b: 40 }, title }}
      config={{ displayModeBar: false, responsive: true }}
    />
  );
}
