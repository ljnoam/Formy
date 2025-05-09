import pandas as pd
from nlp.extractor import extract_info
from nlp.matcher import match_formations

def main():
    print("🧠 Bienvenue sur Formy !")
    user_input = input("Dis-moi ce que tu veux apprendre : ")

    # 1) NLP
    profile = extract_info(user_input)
    print(f"\n✅ Profil détecté : {profile}")

    # 2) Dataset
    df = pd.read_csv("formations_dataset_10000_clean.csv")
    formations = df.to_dict(orient="records")
    print(f"📂 {len(formations)} formations chargées depuis le CSV.")

    # 3) Matching
    print("\n🔍 Recherche des meilleures formations…\n")
    matched = match_formations(profile, formations)

    # 4) Résultat
    if not matched:
        print("❌ Aucune formation trouvée avec ces critères.")
        return

    print("🎯 Formations recommandées :\n")
    for i, f in enumerate(matched, 1):
        succes = f.get("taux_de_succès") or f.get("taux_de_succes") or "N/A"
        score = f.get("_score", "N/A")
        reasons = f.get("_reasons", [])
        reason_cols = ", ".join({col for col, _ in reasons}) if reasons else "N/A"

        print(f"{i}. {f.get('titre', 'Titre inconnu')}")
        print(f"   Thématique   : {f.get('thématique')} / {f.get('sous-thématique')}")
        print(f"   Niveau       : {f.get('niveau')} ({f.get('public_cible')})")
        print(f"   Format       : {f.get('format')} | Langue : {f.get('langue')}")
        print(f"   Certification: {f.get('certification')} | Plateforme : {f.get('plateforme_source')}")
        print(f"   Prix         : {f.get('prix')}€ | Mis à jour : {f.get('date_mise_a_jour')}")
        print(f"   Objectif     : {f.get('objectif_pédagogique')}")
        print(f"   Note         : {f.get('note_utilisateurs')} ⭐ ({f.get('nombre_avis')} avis)")
        print(f"   Succès       : {succes}%")
        print(f"   🔎 Score      : {score} (colonnes matchées : {reason_cols})\n")

if __name__ == "__main__":
    main()
