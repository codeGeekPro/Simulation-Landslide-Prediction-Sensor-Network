import pandas as pd
import numpy as np

def generate_satellite_data(n=50):
    np.random.seed(24)
    data = {
        'timestamp': pd.date_range('2025-06-01', periods=n, freq='6H'),
        'latitude': np.random.uniform(5.0, 7.0, n),
        'longitude': np.random.uniform(-8.0, -6.0, n),
        'sat_humidity': np.random.uniform(15, 95, n),
        'sat_rainfall': np.random.uniform(0, 60, n),
        'ndvi': np.random.uniform(0.2, 0.9, n)
    }
    df = pd.DataFrame(data)
    df.to_csv('data/simulated_satellite.csv', index=False)
    print('Fichier data/simulated_satellite.csv généré.')

if __name__ == '__main__':
    generate_satellite_data(50)
