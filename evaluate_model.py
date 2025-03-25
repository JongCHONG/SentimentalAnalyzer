import joblib
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data.database import get_db_connection
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")

# Charger le modèle et le vectorizer
model = joblib.load("sentiment_model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

# Connexion à la base de données
def get_test_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer un ensemble de test (tweets et labels)
    cursor.execute("SELECT text, positive, negative FROM tweets ORDER BY RAND() LIMIT 200")
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()

    X_test = [row[0] for row in data]  # Texte des tweets
    y_test_positive = [row[1] for row in data]  # Labels positifs
    y_test_negative = [row[2] for row in data]  # Labels négatifs

    return X_test, y_test_positive, y_test_negative

# Récupérer les données de test
X_test, y_test_positive, y_test_negative = get_test_data()

# Vectoriser les tweets
X_test_vectorized = vectorizer.transform(X_test)

# Faire les prédictions
y_pred = model.predict(X_test_vectorized)

# Matrices de confusion
conf_matrix_pos = confusion_matrix(y_test_positive, y_pred)
conf_matrix_neg = confusion_matrix(y_test_negative, y_pred)

# Affichage des matrices de confusion
def plot_confusion_matrix(conf_matrix, title):
    plt.figure(figsize=(6, 4))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Négatif", "Positif"], yticklabels=["Négatif", "Positif"])
    plt.xlabel("Prédictions")
    plt.ylabel("Vérité")
    plt.title(title)
    plt.show()

plot_confusion_matrix(conf_matrix_pos, "Matrice de confusion (Positifs)")
plot_confusion_matrix(conf_matrix_neg, "Matrice de confusion (Négatifs)")

# Calcul des métriques
print("Rapport de classification pour les tweets positifs :")
print(classification_report(y_test_positive, y_pred, target_names=["Négatif", "Positif"]))

print("Rapport de classification pour les tweets négatifs :")
print(classification_report(y_test_negative, y_pred, target_names=["Négatif", "Positif"]))
