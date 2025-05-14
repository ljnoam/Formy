# chatbot_terminal.py

import pandas as pd
from formybot import FormyBot

def main():
    print("🧠 Bienvenue sur FormyBot (mode terminal) !")
    print("Tape 'exit' pour quitter à tout moment.\n")

    # Chargement des formations
    df = pd.read_csv("Formations_dataset_10000_clean.csv")
    formations = df.to_dict(orient="records")
    bot = FormyBot(formations)

    while True:
        user_input = input("👤 Toi : ")

        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 À bientôt !")
            break

        response = bot.handle_input(user_input)
        print(f"🤖 Formy : {response}\n")

if __name__ == "__main__":
    main()
