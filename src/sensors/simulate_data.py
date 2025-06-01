import pandas as pd
import numpy as np

def generate_sensor_data(n=100):
    np.random.seed(42)
    data = {
        'timestamp': pd.date_range('2025-06-01', periods=n, freq='H'),
        'humidity': np.random.uniform(20, 90, n),
        'vibration': np.random.uniform(0, 1, n),
        'rainfall': np.random.uniform(0, 50, n),
        'temperature': np.random.uniform(10, 35, n)
    }
    df = pd.DataFrame(data)
    # Conversion explicite du timestamp en chaîne de caractères pour compatibilité CSV/Streamlit
    df['timestamp'] = df['timestamp'].astype(str)
    df.to_csv('data/simulated_sensors.csv', index=False)
    print('Fichier data/simulated_sensors.csv généré.')

if __name__ == '__main__':
    generate_sensor_data(200)
