import os
import re
import sys
from bs4 import BeautifulSoup

def extraire_video_id(url):
    regex = r'(?:v=|\/v\/|embed\/|youtu\.be\/|\/shorts\/|^)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    return match.group(1) if match else None

def saisie_multiligne(invite):
    print(f"\n[!] {invite}")
    print("(Collez votre code/texte, puis faites ENTREE + CTRL+D pour valider)")
    print("-" * 30)
    contenu = sys.stdin.read()
    print("-" * 30)
    return contenu.strip()

def gerer_dev():
    print("\n--- MOUSSTALL STUDIO : GESTIONNAIRE DEV (MULTI-LINE V2) ---")
    print("1. Ajouter un cours")
    print("2. Supprimer un cours")
    choix = input("Choix (1/2) : ")

    try:
        with open("dev.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        target = soup.find(id="academy-content")

        if choix == "1":
            titre = input("Titre du module Dev : ")
            url_brut = input("Colle le lien YouTube : ")
            video_id = extraire_video_id(url_brut)
            
            if not video_id:
                print("[-] Erreur : Lien YouTube invalide.")
                return

            video_url = f"https://www.youtube.com/embed/{video_id}"
            
            # Saisie de la description (bloque le flux après Ctrl+D)
            description = saisie_multiligne("Description du cours")
            
            # --- CORRECTIF POUR LUBUNTU / LINUX ---
            # On ré-ouvre le clavier pour les prochaines questions
            sys.stdin = open('/dev/tty') 
            
            question = input("Question Quiz : ")
            opt_a = input("Option A : ")
            opt_b = input("Option B : ")
            opt_c = input("Option C : ")
            rep = input("Bonne réponse (A/B/C) : ").upper()

            quiz_id = titre.replace(" ", "_")

            nouveau_cours = f"""
            <div class="module-container" data-title="{titre}">
                <button class="accordion" style="border-left: 4px solid #39ff14;">> DEV_LOG : {titre}</button>
                <div class="panel">
                    <div class="lesson">
                        <h3>{titre}</h3>
                        <p style="white-space: pre-wrap; color: #eee;">{description}</p>
                        <div style="margin: 20px 0; text-align: center;">
                            <iframe width="100%" height="350" src="{video_url}" frameborder="0" allowfullscreen style="border: 1px solid #39ff14; box-shadow: 0 0 15px rgba(57, 255, 20, 0.2);"></iframe>
                        </div>
                        <div class="exercise-box" style="border-left: 3px solid #39ff14;">
                            <h4 style="color: #39ff14;">🎯 TEST_DE_COMPILATION</h4>
                            <p>{question}</p>
                            <ul style="list-style-type: none; padding-left: 0;">
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="A"> A) {opt_a}</label></li>
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="B"> B) {opt_b}</label></li>
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="C"> C) {opt_c}</label></li>
                            </ul>
                            <button class="btn-valider" style="border-color: #39ff14; color: #39ff14;" onclick="verifierAuto(this, '{rep}')">VÉRIFIER LE CODE</button>
                            <p class="resultat-mini"></p>
                        </div>
                    </div>
                </div>
            </div>
            """
            target.append(BeautifulSoup(nouveau_cours, "html.parser"))
            print(f"[+] Module Dev '{titre}' ajouté avec succès.")

        elif choix == "2":
            titre_a_suppr = input("Titre du module à supprimer : ")
            module = soup.find("div", {"data-title": titre_a_suppr})
            if module:
                module.decompose()
                print(f"[+] Module '{titre_a_suppr}' supprimé.")

        with open("dev.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    except Exception as e:
        print(f"[-] Erreur système : {e}")

if __name__ == "__main__":
    gerer_dev()
