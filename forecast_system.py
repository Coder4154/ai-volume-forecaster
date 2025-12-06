# forecast_system.py
# Quantitative AI Statistical Forecasting System - Part 1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class QuantitativeForecaster:
    """
    Quantitative AI forecasting system using statistical mathematics.
    Implements numerical methods and probability theory.
    """

    def __init__(self, data_path):
        """Initialize with historical dataset."""
        self.df = pd.read_csv(data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df.set_index('date', inplace=True)

        # Colors for graphs
        self.colors = {
            'red': '#B22234',
            'white': '#FFFFFF',
            'blue': '#3C3B6E'
        }

        print("\033[91m" + "="*60)
        print("\033[97m" + " 📊 QUANTITATIVE AI FORECASTING SYSTEM 📊")
        print("\033[94m" + "="*60 + "\033[0m")
        print(f"Loaded {len(self.df)} data points")
        print(f"Data dimensionality: {self.df.shape}")

    def quantitative_analysis(self):
        """Perform comprehensive quantitative analysis."""
        print("\n🔍 QUANTITATIVE PATTERN ANALYSIS...\n")

        stats_dict = {
            'mean': self.df['volume'].mean(),
            'variance': self.df['volume'].var(),
            'std_dev': self.df['volume'].std(),
            'skewness': stats.skew(self.df['volume']),
            'kurtosis': stats.kurtosis(self.df['volume']),
            'cv': self.df['volume'].std() / self.df['volume'].mean(),
            'trend_coefficient': np.polyfit(range(len(self.df)), self.df['volume'], 1)[0]
        }

        print("📌 Statistical Summary:")
        for k, v in stats_dict.items():
            print(f"{k:20} → {v:.4f}")

        return stats_dict

    def moving_average_forecast(self, window=7):
        """Simple Moving Average (SMA) forecast."""
        print("\n📘 MOVING AVERAGE FORECAST")
        self.df["sma"] = self.df["volume"].rolling(window=window).mean()

        forecast = self.df["sma"].iloc[-1]
        print(f"Next-day SMA forecast ({window}-day window): {forecast:.2f}")

        return forecast

    def exponential_smoothing(self, alpha=0.3):
        """Single exponential smoothing forecast."""
        print("\n📗 EXPONENTIAL SMOOTHING FORECAST")

        es = [self.df["volume"].iloc[0]]
        for v in self.df["volume"][1:]:
            es.append(alpha * v + (1 - alpha) * es[-1])

        self.df["exp_smoothing"] = es
        forecast = es[-1]

        print(f"Next-day exponential smoothing forecast (alpha={alpha}): {forecast:.2f}")
        return forecast

    def create_visualizations(self):
        """Create and save trend, moving average, and smoothing plots."""
        print("\n📊 Generating visualizations...")

        plt.figure(figsize=(12, 6))
        plt.plot(self.df.index, self.df["volume"], label="Volume", color=self.colors['blue'])

        if "sma" in self.df:
            plt.plot(self.df.index, self.df["sma"], label="7-Day SMA", color=self.colors['red'])

        if "exp_smoothing" in self.df:
            plt.plot(self.df.index, self.df["exp_smoothing"], label="Exp Smoothing", color=self.colors['white'])

        plt.title("Volume Forecasting Visualizations")
        plt.legend()
        plt.grid()
        plt.savefig("forecast_visualization.png")

        print("📁 Saved: forecast_visualization.png")


# =======================
# MAIN EXECUTION SECTION
# =======================

if __name__ == "__main__":
    forecaster = QuantitativeForecaster("data/historical_volumes.csv")

    # Run analysis steps
    forecaster.quantitative_analysis()
    forecaster.moving_average_forecast(window=7)
    forecaster.exponential_smoothing(alpha=0.3)
    forecaster.create_visualizations()
