import unicodedata

def normalize(text):
    if not isinstance(text, str):
        return ""
    return unicodedata.normalize("NFD", text)\
        .encode("ascii", "ignore")\
        .decode("utf-8")\
        .lower().strip()

def preprocess_formation(formation: dict):
    for k, v in formation.items():
        if isinstance(v, str):
            formation[k] = normalize(v)
