import re
import json
import unicodedata
import spacy
from transformers import pipeline
import os

# 1) Chargement du mapping
MAPPING_PATH = os.path.join("data", "label_mapping.json")
with open(MAPPING_PATH, "r", encoding="utf-8") as f:
    MAPPING = json.load(f)["groups"]

def normalize(text):
    if not isinstance(text, str):
        return ""
    return unicodedata.normalize("NFD", text)\
        .encode("ascii", "ignore")\
        .decode("utf-8")\
        .lower().strip()

def get_candidate_labels():
    labels = set()
    for group in MAPPING.values():
        for val_list in group["values"].values():
            labels.update(val_list)
    return list(labels)

def group_labels_by_mapping(labels):
    grouped = {}
    for group_name, group in MAPPING.items():
        grouped[group_name] = []
        for value, aliases in group["values"].items():
            aliases_normalized = [normalize(a) for a in aliases]
            for label in labels:
                if label in aliases_normalized:
                    grouped[group_name].append(label)
    # Nettoyage des groupes vides
    return {k: v for k, v in grouped.items() if v}

def filter_labels(labels):
    filtered = []
    for label in labels:
        if not label or len(label) < 3:
            continue
        if label in ["oui", "non", "fr", "en", "projet", "quiz", "pdf", "podcast"]:
            continue
        if label.startswith("a l'issue de cette formation"):
            continue
        if re.fullmatch(r"[\d\W]+", label):  # uniquement chiffres ou ponctuation
            continue
        filtered.append(label)
    return filtered

# 2) Init NLP
nlp_fr = spacy.load("fr_core_news_md")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CANDIDATE_LABELS = get_candidate_labels()

def extract_info(text: str) -> dict:
    txt_norm = normalize(text)

    result = classifier(txt_norm, CANDIDATE_LABELS, multi_label=True)
    raw_labels = [
        normalize(label) for label, score in zip(result["labels"], result["scores"])
        if score > 0.4
    ]
    filtered = filter_labels(raw_labels)
    grouped = group_labels_by_mapping(filtered)

    print(f"🔍 Labels extraits : {filtered}")
    print(f"🗂 Labels groupés : {grouped}")

    entities = []
    m = re.search(r"(\d+)\s*h", text.lower())
    if m:
        entities.append({"type": "duree_hebdo", "value": int(m.group(1))})

    return {
        "labels": filtered,
        "labels_by_group": grouped,
        "entities": entities
    }
