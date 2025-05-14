from nlp.extractor import extract_info
from nlp.matcher import match_formations
from nlp.preprocess import normalize

def merge_profiles(base, new):
    base['labels'].extend(new.get('labels', []))
    for k, vals in new.get('labels_by_group', {}).items():
        base['labels_by_group'].setdefault(k, []).extend(vals)
    base['labels'] = list(dict.fromkeys(base['labels']))
    for k in base['labels_by_group']:
        base['labels_by_group'][k] = list(dict.fromkeys(base['labels_by_group'][k]))

class FormyBot:
    def __init__(self, formations):
        self.profile = {"labels": [], "labels_by_group": {}}
        self.stage = "start"
        self.formations = formations

    def handle_input(self, user_input):
        print(f"[DEBUG] STAGE = {self.stage}, INPUT = {user_input}")
        user_input = normalize(user_input)

        if self.stage == "start":
            info = extract_info(user_input)
            print(f"[DEBUG] EXTRACTED: {info}")
            merge_profiles(self.profile, info)
            self.stage = "langue"
            return "Tu veux suivre la formation en quelle langue ? (ex : français, anglais)"

        elif self.stage == "langue":
            self.profile["labels_by_group"].setdefault("langues", []).append(user_input)
            self.stage = "format"
            return "Et le format ? (ex : vidéo, projet, pdf...)"

        elif self.stage == "format":
            self.profile["labels_by_group"].setdefault("formats", []).append(user_input)
            self.stage = "niveau"
            return "Quel niveau tu vises ? (débutant, intermédiaire, avancé)"

        elif self.stage == "niveau":
            self.profile["labels_by_group"].setdefault("niveaux", []).append(user_input)
            self.stage = "match"
            return self._format_results()

        elif self.stage == "match":
            return "Si tu veux relancer une recherche, recharge la page ou pose une autre question !"

        return "Hmm… j'ai pas compris, tu peux reformuler ?"

    def _format_results(self):
        print("[DEBUG] Launching match with profile:", self.profile)
        results = match_formations(self.profile, self.formations)
        if not results:
            return "Désolé, j'ai rien trouvé pour toi 😞 Essaie avec d'autres mots clés ou sujets."

        msg = "Voici quelques formations que je te recommande 👇\n"
        for i, f in enumerate(results, 1):
            titre = f.get("titre", "Sans titre")
            plateforme = f.get("plateforme_source", "Inconnue")
            niveau = f.get("niveau", "N/A")
            prix = f.get("prix", "Gratuit")
            lien = f.get("url", None)

            msg += f"**{i}. {titre}**\n"
            msg += f"   - Plateforme : {plateforme} | Niveau : {niveau} | Prix : {prix}€\n"
            if lien:
                msg += f"   - 🔗 [Voir la formation]({lien})\n"
            msg += "\n"
        return msg
