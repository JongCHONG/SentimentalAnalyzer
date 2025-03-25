import joblib
import mysql.connector
import nltk
import datetime
import os
from data.database import get_db_connection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords

nltk.download("stopwords")

# Fonction pour récupérer la date du dernier entraînement
def get_last_training_date():
    if os.path.exists("last_training.txt"):
        with open("last_training.txt", "r") as file:
            return file.read().strip()
    return None

# Fonction pour mettre à jour la date du dernier entraînement
def update_last_training_date():
    with open("last_training.txt", "w") as file:
        file.write(str(datetime.datetime.now()))

# Fonction pour récupérer uniquement les nouveaux tweets
def get_training_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    last_training_date = get_last_training_date()

    if last_training_date:
        query = "SELECT text, positive FROM tweets WHERE date_added > %s"
        cursor.execute(query, (last_training_date,))
    else:
        query = "SELECT text, positive FROM tweets"
        cursor.execute(query)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    X_train = [row[0] for row in data]
    y_train = [row[1] for row in data]

    return X_train, y_train

# Fonction principale d'entraînement
def model_training():
    X_train, y_train = get_training_data()

    if not X_train:
        return "Aucun nouveau tweet à entraîner."

    print(f"Réentraînement avec {len(X_train)} tweets...")

    # Vérifiez les classes dans y_train
    unique_classes = set(y_train)
    print(f"Classes présentes dans les données d'entraînement : {unique_classes}")

    if len(unique_classes) < 2:
        return "Les données d'entraînement doivent contenir au moins deux classes différentes. (positif et négatif)"

    # Vectorisation et réentraînement du modèle
    vectorizer = CountVectorizer(stop_words=stopwords.words("french"))
    X_train_vectorized = vectorizer.fit_transform(X_train)

    model = LogisticRegression()
    model.fit(X_train_vectorized, y_train)

    # Sauvegarde du modèle mis à jour
    joblib.dump(model, "sentiment_model.joblib")
    joblib.dump(vectorizer, "vectorizer.joblib")

    update_last_training_date()
    return "Modèle réentraîné avec succès avec les nouveaux tweets."

# Permet d'exécuter le script manuellement aussi
if __name__ == "__main__":
    print(model_training())
