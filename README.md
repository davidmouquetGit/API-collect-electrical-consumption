# API pour collecter les données de consommations électrique d'ENEDIS et les données météo

# 🔥 Prédiction de la Consommation Électrique

> Prédire la consommation électrique horaire à partir de données météo et de données d’occupation des bâtiments.

---

## 🎯 Objectif du projet

Ce projet vise à construire un modèle de machine learning capable d’estimer la consommation électrique d’un site à partir de paramètres externes (température, humidité, occupation, etc.).  
L’objectif est de mieux anticiper les pics de consommation et optimiser les coûts énergétiques.

---

## 📊 Données utilisées

- **Source :** Données internes + API météo (OpenWeatherMap)  
- **Format :** CSV / JSON  
- **Volume :** ~500 000 enregistrements horaires  
- **Variables clés :** température, taux d’occupation, jour de la semaine, heure, consommation  

---

## ⚙️ Méthodologie

1. Nettoyage et agrégation des données (pandas, SQLAlchemy)  
2. Feature engineering et scaling  
3. Entraînement de modèles (RandomForest, XGBoost, LSTM)  
4. Évaluation via RMSE / MAPE  
5. Visualisation interactive avec **Streamlit**

---

## 🚀 Résultats

- Meilleur modèle : **XGBoost**  
- **RMSE : 0.37**  
- **Gain de 12%** par rapport au modèle de base  
- Application Streamlit déployée sur EC2  

![Dashboard](images/dashboard.png)

---

## 🗂️ Structure du dépôt

