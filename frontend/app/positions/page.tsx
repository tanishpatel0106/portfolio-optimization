import { ExposureBreakdown } from "../../components/ExposureBreakdown";
import { PositionChangesTable } from "../../components/PositionChangesTable";

export default function PositionsPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Positions & Blotter</h2>
      <div className="grid gap-4 md:grid-cols-3">
        <ExposureBreakdown
          title="Exposure by Region"
          items={[
            { label: "US", value: "52%" },
            { label: "EU", value: "24%" },
            { label: "JP", value: "14%" }
          ]}
        />
        <ExposureBreakdown
          title="Exposure by Currency"
          items={[
            { label: "USD", value: "62%" },
            { label: "EUR", value: "18%" },
            { label: "JPY", value: "12%" }
          ]}
        />
        <ExposureBreakdown
          title="Exposure by Asset Class"
          items={[
            { label: "Equity", value: "70%" },
            { label: "ETF", value: "30%" }
          ]}
        />
      </div>
      <PositionChangesTable
        rows={[
          { date: "2024-06-02", ticker: "AAPL", action: "Added to long", delta: "+5" },
          { date: "2024-06-03", ticker: "EWJ", action: "Opened new position", delta: "+10" }
        ]}
      />
    </div>
  );
}
