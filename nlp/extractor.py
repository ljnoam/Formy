import re
import json
import unicodedata
import os

# Lazy loading
nlp_fr = None
classifier = None
CANDIDATE_LABELS = None

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

def lazy_init():
    global nlp_fr, classifier, CANDIDATE_LABELS
    if nlp_fr is None:
        import spacy
        nlp_fr = spacy.load("fr_core_news_md")
    if classifier is None:
        from transformers import pipeline
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    if CANDIDATE_LABELS is None:
        CANDIDATE_LABELS = get_candidate_labels()

def group_labels_by_mapping(labels):
    grouped = {}
    for group_name, group in MAPPING.items():
        grouped[group_name] = []
        for value, aliases in group["values"].items():
            aliases_norm = [normalize(a) for a in aliases]
            for label in labels:
                if label in aliases_norm:
                    grouped[group_name].append(value)
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
        if re.fullmatch(r"[\d\W]+", label):
            continue
        filtered.append(label)
    return filtered

def expand_synonyms(labels, threshold=0.75):
    lazy_init()
    out = set(labels)
    for lbl in labels:
        tok = nlp_fr(lbl)[0]
        for w in nlp_fr.vocab:
            if w.has_vector and tok.has_vector and tok.similarity(w) > threshold:
                out.add(w.text)
    return list(out)

def extract_info(text: str) -> dict:
    lazy_init()
    txt_norm = normalize(text)
    result = classifier(txt_norm, CANDIDATE_LABELS, multi_label=True)
    raw = [normalize(l) for l, s in zip(result["labels"], result["scores"]) if s > 0.4]
    filtered = filter_labels(raw)
    expanded = expand_synonyms(filtered)
    grouped = group_labels_by_mapping(expanded)

    # Extraction d'entités simples
    entities = []
    m = re.search(r"(\d+)\s*h", text.lower())
    if m:
        entities.append({"type": "duree_hebdo", "value": int(m.group(1))})

    return {
        "labels": filtered,
        "labels_by_group": grouped,
        "entities": entities
    }
