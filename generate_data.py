import pandas as pd
import numpy as np

# Generate dates for 13 months starting Dec 1, 2024
dates = pd.date_range(start='2024-12-01', periods=395, freq='D')

# Generate random volumes between 90 and 150
volumes = np.random.randint(90, 151, size=len(dates))

# Create DataFrame
df = pd.DataFrame({'Date': dates, 'Volume': volumes})

# Save to CSV
df.to_csv('data.csv', index=False)
print("data.csv created with 13 months of daily data.")
