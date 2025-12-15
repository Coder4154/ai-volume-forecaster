iimport pandas as pd

def run_forecast(input_file):
    # Read CSV
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: '{input_file}' is empty or invalid.")
        return

    # Validate columns
    if 'Date' not in df.columns or 'Volume' not in df.columns:
        print("Error: CSV must contain 'Date' and 'Volume' columns.")
        return

    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Ensure 'Volume' is numeric
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    
    # Drop rows with invalid volume
    df = df.dropna(subset=['Volume'])
    
    if df.empty:
        print("Error: No valid data found in CSV.")
        return

    print("Input data preview:")
    print(df.head())

    # Average of historical volumes
    avg_volume = int(df['Volume'].mean())

    # Generate 13 months of future dates (~395 days)
    future_dates = pd.date_range(start=df['Date'].max() + pd.Timedelta(days=1), periods=395)

    # Create forecast
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Forecasted_Volume': [avg_volume] * len(future_dates)
    })

    # Save to CSV
    forecast_df.to_csv('forecast_output.csv', index=False)
    print(f"Forecast saved to 'forecast_output.csv'.")
    print(forecast_df.head())

if __name__ == "__main__":
    input_file = 'data.csv'
    run_forecast(input_file)
