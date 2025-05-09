import json
from nlp.preprocess import preprocess_formation

with open("data/label_mapping.json", "r", encoding="utf-8") as f:
    LABEL_MAPPING = json.load(f)["groups"]

QUALITY_KEYS = ["note_utilisateurs", "nombre_avis", "taux_de_succès", "taux_de_succes"]

def has_match(formation, col, aliases):
    val = str(formation.get(col, "")).lower()
    return any(alias in val for alias in aliases)

def score_quality(formation):
    note = float(formation.get("note_utilisateurs") or 0)
    avis = int(formation.get("nombre_avis") or 0)
    taux = float(formation.get("taux_de_succès") or formation.get("taux_de_succes") or 0)
    return (note / 5) * 40 + min(avis, 500) / 500 * 30 + (taux / 100) * 30

def match_formations(profile, formations):
    labels_by_group = profile.get("labels_by_group", {})
    all_labels = profile.get("labels", [])

    # Normalisation
    for f in formations:
        preprocess_formation(f)

    current = formations.copy()

    # --- Étape 1 : filtre strict sur thématique/sous-thématique ---
    priority_labels = set(labels_by_group.get("domaines", []) + labels_by_group.get("sous-domaines", []))
    print(f"🎯 Filtrage prioritaire sur : {priority_labels}")

    if priority_labels:
        current = [
            f for f in current if (
                has_match(f, "thématique", priority_labels)
                or has_match(f, "sous-thématique", priority_labels)
            )
        ]
        print(f"🧩 {len(current)} formations après filtrage thématique.")

    # --- Étape 2 : filtrage progressif via les autres colonnes ---
    label_to_cols = {}
    for group_name, labels in labels_by_group.items():
        for value in labels:
            for col in LABEL_MAPPING[group_name]["columns"]:
                label_to_cols.setdefault(col, set()).add(value)

    if not current or not label_to_cols:
        print("❌ Pas assez de données pour matcher.")
        return []

    print(f"📌 Colonnes de filtrage secondaires : {list(label_to_cols.keys())}")

    matching = []
    for f in current:
        reasons = []
        for col, aliases in label_to_cols.items():
            if has_match(f, col, aliases):
                reasons.append((col, list(aliases)))
        if reasons:
            f["_reasons"] = reasons
            matching.append(f)

    print(f"🔎 {len(matching)} formations matchées après filtres secondaires.")

    if len(matching) > 5:
        for f in matching:
            f["_score"] = round(score_quality(f), 2)
        matching = sorted(matching, key=lambda x: x["_score"], reverse=True)

    print(f"✅ Résultat final : {len(matching)} formations.")
    return matching[:5]
