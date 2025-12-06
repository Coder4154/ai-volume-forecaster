import os
from forecast_system import QuantitativeForecaster

def test_data_exists():
    assert os.path.exists("data/historical_volumes.csv")

def test_load_data():
    forecaster = QuantitativeForecaster("data/historical_volumes.csv")
    assert len(forecaster.df) > 100

def test_moving_average():
    forecaster = QuantitativeForecaster("data/historical_volumes.csv")
    forecast = forecaster.moving_average_forecast(window=7)
    assert forecast > 0

def test_exponential_smoothing():
    forecaster = QuantitativeForecaster("data/historical_volumes.csv")
    forecast = forecaster.exponential_smoothing(alpha=0.3)
    assert forecast > 0
