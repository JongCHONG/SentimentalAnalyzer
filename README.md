```md
# 🧠 API d'Analyse de Sentiments avec Flask & Machine Learning

Ce projet est une API Flask permettant d'analyser les sentiments de tweets en utilisant un modèle de **Régression Logistique**.  
L'API est connectée à une base **MySQL** et supporte le **réentraînement automatique** avec de nouvelles données.

---

## 🚀 Fonctionnalités

✅ **Analyse des sentiments** d'une liste de tweets (`/analyze`)  
✅ **Stockage des tweets** annotés en base MySQL  
✅ **Réentraînement automatique** du modèle (`/training`)  
✅ **Évaluation des performances** avec matrices de confusion  

---

## 📌 Installation & Configuration

### 1️⃣ **Cloner le projet**
```bash
git clone https://github.com/JongCHONG/EfreiM2AlgoTP.git
cd EfreiM2AlgoTP
```

### 2️⃣ **Installer les dépendances**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Configurer MySQL**
Créer la base de données et la table :
```sql
CREATE DATABASE sentiment_analysis;
USE sentiment_analysis;

CREATE TABLE tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive INT NOT NULL,
    negative INT NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Lancer l'API

### **Démarrer le serveur Flask**
```bash
python app.py
```
L'API sera accessible sur :  
🔗 `http://127.0.0.1:5000/`

---

## 🔥 Utilisation de l'API

### **1️⃣ Analyser les sentiments**
- **Endpoint** : `POST /analyze`
- **Requête JSON** :
```json
{
  "tweets": ["J'adore ce produit !", "C'est une honte.", "Je suis mitigé."]
}
```
- **Réponse JSON** :
```json
{
  "J'adore ce produit !": "Positif",
  "C'est une honte.": "Négatif",
  "Je suis mitigé.": "Négatif"
}
```

### **2️⃣ Récupérer les tweets stockés**
- **Endpoint** : `GET /tweets`
- **Réponse JSON** :
```json
[
  {"id": 1, "text": "J'adore ce produit !", "positive": 1, "negative": 0, "date_added": "2024-03-24 12:00:00"},
  {"id": 2, "text": "C'est une honte.", "positive": 0, "negative": 1, "date_added": "2024-03-24 12:05:00"}
]
```

### **3️⃣ Réentraîner le modèle**
- **Endpoint** : `POST /training`
- **Réponse JSON** :
```json
{"message": "Modèle réentraîné avec succès avec les nouveaux tweets."}
```

---

## 📊 Évaluation du modèle
Lance le script d’évaluation pour générer les matrices de confusion et calculer la précision, le rappel et le F1-score.
```bash
python evaluate_model.py
```
Cela affichera les **métriques du modèle** et générera un **rapport en PDF**.

---

## 📅 Automatiser le réentraînement
Ajoute cette ligne dans **crontab** pour exécuter le réentraînement **chaque lundi à 3h du matin** :
```bash
0 3 * * 1 /usr/bin/python3 /chemin/vers/ton/projet/model_training.py

Ex:
* * * * * /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 /Users/chongjonghoa/Desktop/EfreiM2AlgoTP/model_training.py >> /Users/chongjonghoa/Desktop/EfreiM2AlgoTP/cron.log 2>&1
```
Vérifie les logs avec :
```bash
cat cron_log.txt
```

## 🏆 Auteurs
👨‍💻 **CHONG Jong Hoa** – Développeur du projet  
📧 Contact : [jochong27@gmail.com](mailto:jochong27@gmail.com)
```
