from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans


def detect_regimes(returns: pd.Series, window: int = 63, k: int = 3) -> pd.DataFrame:
    rolling_vol = returns.rolling(window).std()
    rolling_ret = returns.rolling(window).mean()
    drawdown = (1 + returns).cumprod() / (1 + returns).cumprod().cummax() - 1
    features = pd.concat([rolling_vol, rolling_ret, drawdown], axis=1).dropna()
    if features.empty:
        return pd.DataFrame(columns=["date", "regime"])
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = model.fit_predict(features)
    result = pd.DataFrame({"date": features.index, "regime": labels})
    return result
