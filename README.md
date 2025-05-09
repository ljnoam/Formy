
# 📚 Formy – Moteur intelligent de recommandation de formations

Formy est un moteur de recherche intelligent de formations, basé sur l’analyse de langage naturel (NLP) et un système de matching multicritères.  
Il permet à un utilisateur de décrire librement ce qu’il veut apprendre (ex: *"Je veux apprendre la cybersécurité en français"*) et reçoit en retour les meilleures formations issues d’un dataset.

---

## 📁 Structure du projet

```
Formy/
│
├── main.py                      # Script principal à exécuter
├── requirements.txt            # Dépendances Python à installer
├── formations_dataset_10000_clean.csv  # Base de données des formations (CSV)
│
├── data/
│   └── label_mapping.json      # Mapping entre labels NLP et colonnes du dataset
│
└── nlp/
    ├── extractor.py            # Extraction des mots-clés depuis la phrase utilisateur (NLP)
    ├── matcher.py              # Système de matching intelligent (filtrage + scoring)
    └── preprocess.py           # Fonctions utilitaires de nettoyage et normalisation
```

---

## ⚙️ Installation (1ère fois)

### 1. Clone ou copie du dossier `Formy`
Assure-toi d’avoir **Python 3.8+** installé sur ta machine.

```bash
cd Formy
```

### 2. Crée un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Installe les dépendances Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Télécharge les modèles SpaCy (langue française)

```bash
python -m spacy download fr_core_news_md
```

---

## 🚀 Lancer le projet

Dans le terminal (avec l’environnement activé), exécute :

```bash
python main.py
```

🧠 Tu peux alors taper une phrase comme :

```
Je veux apprendre la cybersécurité en vidéo, niveau intermédiaire, en français.
```

Formy affichera alors les **5 meilleures formations matchées** selon :
- la thématique demandée
- le format et la langue
- le niveau de difficulté
- les notes utilisateurs et taux de réussite
- les certifications disponibles

---

## 🔍 Fonctionnement interne

### 🔹 NLP (`extractor.py`)
- Utilise `transformers` pour faire du **zero-shot classification** à partir d’un mapping défini dans `label_mapping.json`
- Classe les labels extraits par catégories : domaines, formats, langues, niveaux, etc.
- Supprime les labels parasites génériques (`"oui"`, `"en"`, etc.)

### 🔹 Matching (`matcher.py`)
- Filtrage prioritaire sur les colonnes `thématique` et `sous-thématique`
- Puis filtrage secondaire sur les colonnes secondaires (`langue`, `certification`, `format`, etc.)
- Si trop de formations sont encore présentes, un **scoring qualité** est appliqué :  
  (note/5) × 40 + (avis/500) × 30 + (taux de succès/100) × 30

---

## 🧪 Tester avec un petit dataset

Si tu veux tester rapidement le système, tu peux remplacer le fichier `formations_dataset_10000_clean.csv` par une version allégée avec 1000 lignes.

---

## 💡 Améliorations possibles

- Ajouter une **interface web** (ex: Flask + HTML)
- Logger les interactions utilisateurs
- Gérer les synonymes ou champs lexicaux
- Apprendre du feedback utilisateur

---





Projet développé par l’équipe Étudiant ECE – promo 2026  
