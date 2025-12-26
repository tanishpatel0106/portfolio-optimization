import ExposureBreakdown from '../../components/ExposureBreakdown';
import PositionChangesTable from '../../components/PositionChangesTable';

const changes = [
  { date: '2024-05-10', ticker: 'AAPL', action: 'Added to long', delta: '+50' },
  { date: '2024-05-12', ticker: 'EURUSD', action: 'Covered short', delta: '+10000' },
];

export default function PositionsPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Positions & Blotter</h2>
      <div className="grid gap-4 lg:grid-cols-3">
        <ExposureBreakdown
          title="Exposure by Currency"
          items={[
            { label: 'USD', value: '62%' },
            { label: 'EUR', value: '18%' },
            { label: 'JPY', value: '12%' },
          ]}
        />
        <ExposureBreakdown
          title="Exposure by Region"
          items={[
            { label: 'US', value: '55%' },
            { label: 'EU', value: '22%' },
            { label: 'JP', value: '13%' },
          ]}
        />
        <ExposureBreakdown
          title="Gross vs Net"
          items={[
            { label: 'Gross', value: '1.45x' },
            { label: 'Net', value: '0.92x' },
          ]}
        />
      </div>
      <PositionChangesTable rows={changes} />
    </div>
  );
}
