# 🤖 FormyBot – Chatbot de recommandation de formations

FormyBot est un assistant conversationnel intelligent qui aide les utilisateurs à trouver des formations en ligne en fonction de leurs objectifs, préférences et contraintes.  
Il s’appuie sur du **traitement du langage naturel (NLP)** et un moteur de **matching sémantique** pour proposer les formations les plus pertinentes.

---

## 🚀 Fonctionnalités principales

- 💬 Interface conversationnelle (actuellement en terminal)
- 🧠 Analyse automatique des intentions et préférences via NLP
- 🎯 Recommandation intelligente de formations depuis un dataset de 10 000+
- 🌐 Multilingue, multi-format, tous niveaux
- ⚡ Optimisé pour fonctionner **localement sur CPU**

---

## 🛠️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/toncompte/formybot.git
cd formybot
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# ou
source venv/bin/activate  # Mac/Linux
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
python -m spacy download fr_core_news_md
```

---

## ▶️ Lancement du chatbot (mode terminal)

```bash
python chatbot_terminal.py
```

Vous pouvez alors discuter avec le bot :
```
👤 Toi : Salut, j’aimerais apprendre la cybersécurité
🤖 Formy : Tu veux suivre la formation en quelle langue ? ...
```

Tapez `exit` pour quitter.

---

## 🧠 Comment fonctionne le NLP ?

Le NLP repose sur deux technologies principales :

### 🔹 `spaCy` (modèle français `fr_core_news_md`)
- Utilisé pour l’expansion de synonymes
- Aide à enrichir les labels extraits

### 🔹 `transformers` – modèle `facebook/bart-large-mnli`
- Pipeline `zero-shot-classification`
- Permet de classer n'importe quel texte utilisateur parmi une **centaine de labels candidats**
- Exemple : "Je veux un travail dans la cybersécurité" ➝ détecte `cybersécurité`, `cryptographie`, etc.

> ⚠️ Pour optimiser la vitesse, le chargement du modèle est "lazy" = il ne s'initialise qu'à la première demande.

---

## 📊 Données utilisées

Le fichier `formations_dataset_10000_clean.csv` contient toutes les formations disponibles.

Chaque formation a les colonnes suivantes :
- `titre`
- `thématique` / `sous-thématique`
- `niveau`
- `format`
- `langue`
- `certification`
- `plateforme_source`
- `note_utilisateurs`, `nombre_avis`, `taux_de_succès`

---

## 🤖 Fonctionnement du chatbot (`formybot.py`)

### Étapes de dialogue :
1. L'utilisateur exprime son besoin librement
2. Le NLP extrait les **labels** et **entités**
3. Le bot demande des infos complémentaires :
   - Langue
   - Format
   - Niveau
4. Ensuite il déclenche un `matching`
5. Les résultats sont affichés avec :
   - Titre, plateforme, niveau, prix, lien

### Exemple :
```
👤 Toi : Je veux apprendre le machine learning
🤖 Formy : Tu veux suivre la formation en quelle langue ?
...
```

---

## ⚙️ Matching intelligent (`matcher.py`)

- Le matching compare le **profil utilisateur** avec le dataset de formations.
- Un **filtrage prioritaire** est appliqué sur la thématique
- Puis un **filtrage secondaire** (langue, format, niveau…)
- Les résultats sont **triés par qualité** (note, avis, taux de succès)

---

## 🧪 Tester manuellement le NLP

Vous pouvez tester directement le module NLP :

```python
from nlp.extractor import extract_info

text = "Je cherche une formation en cybersécurité, plutôt débutant"
print(extract_info(text))
```

Cela renverra un dictionnaire avec :
- `labels`
- `labels_by_group`
- `entities` (ex: "10h/semaine", "objectif pro", etc.)

---

## 📁 Arborescence du projet

```
formybot/
├── chatbot_terminal.py       # Interface terminal
├── formybot.py               # Logique du chatbot
├── requirements.txt          # Dépendances Python
├── formations_dataset_10000_clean.csv
├── data/
│   └── label_mapping.json    # Regroupe les synonymes et les mappings NLP
├── nlp/
│   ├── extractor.py          # Traitement NLP + classification
│   ├── matcher.py            # Système de recommandation
│   ├── preprocess.py         # Nettoyage de texte
└── .gitignore
```

---

## ✅ À venir (ou bonus)

- Interface Web avec React ou Streamlit
- Reset de la session via `reset`
- Gestion de plusieurs utilisateurs
- Enrichissement du dataset

---

## 📞 Contact

Projet réalisé dans le cadre du module **Mise en Situation Professionnelle 2025 – ECE Paris**  
Équipe : Noam + collaborateurs  
Encadrant : [Nom du prof]