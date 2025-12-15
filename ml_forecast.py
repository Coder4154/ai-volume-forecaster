# ml_forecast.py
# Quantitative AI - Machine Learning Forecasting Module (Week 8)

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore")


class QuantitativeMLForecaster:
    """
    Quantitative Machine Learning implementation for numerical forecasting
    Applies mathematical learning algorithms and statistical validation
    """

    def __init__(self, data_path):
        """Initialize with historical dataset"""
        self.df = pd.read_csv(data_path)
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df.set_index("date", inplace=True)

        self.models = {}
        self.metrics = {}
        self.test_predictions = {}

        print("\033[91m" + "=" * 60)
        print("\033[97m" + " 🤖 QUANTITATIVE ML FORECASTER 🤖")
        print("\033[94m" + "=" * 60 + "\033[0m")

    # =====================================================
    # FEATURE ENGINEERING
    # =====================================================
    def engineer_quantitative_features(self, window=30):
        """Create numerical features using mathematical transformations"""

        df = self.df.copy()

        # Lag features
        for i in range(1, window + 1):
            df[f"lag_{i}"] = df["volume"].shift(i)

        # Rolling statistics
        df["rolling_mean_7"] = df["volume"].rolling(7).mean()
        df["rolling_mean_30"] = df["volume"].rolling(30).mean()
        df["rolling_std_7"] = df["volume"].rolling(7).std()
        df["rolling_std_30"] = df["volume"].rolling(30).std()

        # Mathematical transforms
        df["log_volume"] = np.log1p(df["volume"])
        df["sqrt_volume"] = np.sqrt(df["volume"])
        df["volume_squared"] = df["volume"] ** 2

        # Time encoding
        df["day_of_week"] = df.index.dayofweek
        df["month"] = df.index.month
        df["quarter"] = df.index.quarter
        df["time_index"] = range(len(df))

        # Cyclical encoding
        df["day_sin"] = np.sin(2 * np.pi * df.index.dayofyear / 365)
        df["day_cos"] = np.cos(2 * np.pi * df.index.dayofyear / 365)

        df = df.dropna()

        print(f"\n📊 Engineered {df.shape[1] - 1} quantitative features")
        print(f"📈 Sample size after lags: {len(df)}")

        return df

    # =====================================================
    # MODEL TRAINING
    # =====================================================
    def train_models(self, test_size=90):
        """Train ML models with time-series split"""

        df = self.engineer_quantitative_features()

        X = df.drop(columns=["volume"])
        y = df["volume"]

        split = len(df) - test_size
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]

        # -------- Linear Regression --------
        print("\n📈 Training Linear Regression...")
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        lr_pred = lr.predict(X_test)

        # -------- Random Forest --------
        print("🌲 Training Random Forest...")
        rf = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        rf.fit(X_train, y_train)
        rf_pred = rf.predict(X_test)

        # -------- XGBoost --------
        print("🚀 Training XGBoost...")
        xgb_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        xgb_model.fit(X_train, y_train)
        xgb_pred = xgb_model.predict(X_test)

        self.models = {
            "Linear Regression": lr,
            "Random Forest": rf,
            "XGBoost": xgb_model
        }

        self.test_predictions = {
            "Actual": y_test,
            "Linear Regression": lr_pred,
            "Random Forest": rf_pred,
            "XGBoost": xgb_pred
        }

        self._calculate_metrics()

    # =====================================================
    # METRICS
    # =====================================================
    def _calculate_metrics(self):
        """Calculate quantitative performance metrics"""

        print("\n📐 MODEL PERFORMANCE METRICS")

        y_true = self.test_predictions["Actual"]

        for model, preds in self.test_predictions.items():
            if model == "Actual":
                continue

            mae = mean_absolute_error(y_true, preds)
            rmse = np.sqrt(mean_squared_error(y_true, preds))
            r2 = r2_score(y_true, preds)

            self.metrics[model] = {
                "MAE": mae,
                "RMSE": rmse,
                "R²": r2
            }

            print(f"\n{model}")
            print(f"  MAE : {mae:.2f}")
            print(f"  RMSE: {rmse:.2f}")
            print(f"  R²  : {r2:.4f}")


# =====================================================
# MAIN EXECUTION
# =====================================================
if __name__ == "__main__":
    forecaster = QuantitativeMLForecaster("data/historical_volumes.csv")
    forecaster.train_models()
