import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_fallback_price_data(days=63):
    end_date = datetime.today()
    dates = [end_date - timedelta(days=x) for x in range(days)]
    dates.reverse()

    base_price = 100
    prices = []
    for i in range(days):
        change = np.random.normal(0.002, 0.02)
        if i == 0: prices.append(base_price)
        else: prices.append(prices[-1] * (1 + change))
    
    data = {
        'Open': prices,
        'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'Close': prices,
        'Volume': [int(np.random.uniform(100000, 1000000)) for _ in range(days)],
    }
    df = pd.DataFrame(data, index=pd.to_datetime(dates))
    return df
