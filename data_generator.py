# data_generator.py
# Quantitative AI: Generate synthetic numerical data with mathematical patterns

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def generate_volume_data():
    """
    Generate 3 years of numerical volume data using mathematical functions.
    Demonstrates quantitative data synthesis for AI training.
    Includes deterministic and stochastic components.
    """
    # Create numerical date range
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    n_days = len(dates)

    # 1. Linear trend component (mathematical growth function)
    trend = np.linspace(1000, 1500, n_days)

    # 2. Sinusoidal seasonal component
    seasonal_year = 200 * np.sin(2 * np.pi * np.arange(n_days) / 365)

    # 3. Weekly pattern (weekdays vs weekends)
    weekly = np.array([150 if d.weekday() < 5 else 50 for d in dates])

    # 4. Monthly spike (end-of-month uplift)
    monthly = np.array([100 if d.day > 25 else 0 for d in dates])

    # 5. Gaussian noise
    np.random.seed(42)
    noise = np.random.normal(0, 50, n_days)

    # Combine mathematically
    volume = trend + seasonal_year + weekly + monthly + noise
    volume = np.maximum(volume, 0)

    # Build dataset
    df = pd.DataFrame({
        'date': dates,
        'volume': volume.round().astype(int),
        'day_of_week': [d.day_name() for d in dates],
        'month': [d.month for d in dates],
        'year': [d.year for d in dates]
    })

    # Display banner
    print("\033[91m" + "="*50)
    print("\033[97m" + " 🇺🇸 QUANTITATIVE AI DATA GENERATOR 🇺🇸")
    print("\033[94m" + "="*50 + "\033[0m")

    print(f"Generated {len(df)} data points")
    print(f"Date range: {start_date.date()} → {end_date.date()}")
    print(f"Mean (μ): {df['volume'].mean():.2f}")
    print(f"Std Dev (σ): {df['volume'].std():.2f}")
    print(f"Coefficient of Variation: {(df['volume'].std()/df['volume'].mean()):.3f}")

    return df

if __name__ == "__main__":
    data = generate_volume_data()
    data.to_csv("data/historical_volumes.csv", index=False)
    print("\n\033[92m✓ Data saved to data/historical_volumes.csv\033[0m")
