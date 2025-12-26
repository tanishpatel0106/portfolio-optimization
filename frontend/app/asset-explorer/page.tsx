import OHLCVChart from '../../components/OHLCVChart';
import { sampleOhlcv } from '../../lib/sampleData';

export default function AssetExplorerPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Asset Explorer</h2>
      <OHLCVChart data={sampleOhlcv} title="Selected Asset OHLCV" />
    </div>
  );
}
