import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Landslide IoT Dashboard", layout="wide")
st.title("🌍 Landslide Prediction Sensor Network - Dashboard")

# Chargement des données simulées
def load_data():
    try:
        df = pd.read_csv('data/simulated_sensors.csv')
    except FileNotFoundError:
        st.error("Fichier de données non trouvé. Veuillez lancer la simulation.")
        return None
    return df

data = load_data()
# Ajout du chargement des données satellites

def load_satellite_data():
    try:
        df = pd.read_csv('data/simulated_satellite.csv')
    except FileNotFoundError:
        st.warning("Fichier de données satellites non trouvé. Veuillez lancer la simulation.")
        return None
    return df

sat_data = load_satellite_data()

if data is not None:
    st.subheader("Données capteurs (extrait)")
    st.dataframe(data.tail(10))

    # Simulation d'un modèle prédictif simple
    X = data[['humidity', 'vibration', 'rainfall', 'temperature']]
    # Génération de labels fictifs pour la démo
    y = np.random.choice(['faible', 'moyen', 'élevé'], len(X))
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    data['risk_pred'] = model.predict(X)

    # Conversion explicite de la colonne 'risk_pred' en valeurs numériques pour l'affichage
    risk_map = {'faible': 0, 'moyen': 1, 'élevé': 2}
    data['risk_pred_num'] = data['risk_pred'].map(risk_map)

    st.subheader("Prédiction du risque de glissement de terrain")
    st.line_chart(
        data.set_index('timestamp')[['humidity', 'rainfall', 'risk_pred_num']],
        y=['humidity', 'rainfall', 'risk_pred_num']
    )

    st.write("**Légende risque** : faible (0, vert), moyen (1, orange), élevé (2, rouge)")

    st.subheader("Distribution des niveaux de risque prédits")
    st.bar_chart(data['risk_pred'].value_counts())

    st.subheader("Carte géographique des points satellites")
    if sat_data is not None:
        m = folium.Map(location=[sat_data['latitude'].mean(), sat_data['longitude'].mean()], zoom_start=8)
        for _, row in sat_data.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                popup=f"Humidité: {row['sat_humidity']:.1f}%\nPrécipitations: {row['sat_rainfall']:.1f}mm",
                color='blue',
                fill=True,
                fill_opacity=0.6
            ).add_to(m)
        st_folium(m, width=700, height=400)
    else:
        st.info("Veuillez d'abord générer les données satellites.")

    st.success("Simulation et prévisualisation terminées !")
else:
    st.info("Veuillez d'abord générer les données simulées.")
