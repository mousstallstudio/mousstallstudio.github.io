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
    print("(Collez votre texte, puis faites ENTREE puis CTRL+D pour valider)")
    print("-" * 30)
    contenu = sys.stdin.read()
    print("-" * 30)
    return contenu.strip()

def gerer_dev():
    print("\n--- MOUSSTALL STUDIO : GESTIONNAIRE DEV (V4.1) ---")
    print("1. Ajouter un cours")
    print("2. Supprimer un cours")
    choix = input("Choix (1/2) : ")

    try:
        if not os.path.exists("dev.html"):
            print("[-] Erreur : dev.html introuvable.")
            return

        with open("dev.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        target = soup.find(id="academy-content")

        if choix == "1":
            titre = input("Titre du module Dev : ")
            url_brut = input("Lien YouTube : ")
            video_id = extraire_video_id(url_brut)
            
            if not video_id:
                print("[-] Erreur : Lien YouTube invalide.")
                return

            video_url = f"https://www.youtube.com/embed/{video_id}"
            description = saisie_multiligne("Description du cours")

            sys.stdin = open('/dev/tty') 
            
            question = input("Question Quiz : ")
            opt_a = input("Option A : ")
            opt_b = input("Option B : ")
            opt_c = input("Option C : ")
            rep = input("Bonne réponse (A/B/C) : ").upper()

            quiz_id = titre.replace(" ", "_")

            # --- STRUCTURE OPTIMISÉE POUR TA FONCTION verifierAuto ---
            nouveau_html = f"""
            <div class="module-container" data-title="{titre}">
                <button class="accordion" style="border-left: 4px solid #39ff14;">> DEV_LOG : {titre}</button>
                <div class="panel">
                    <div class="lesson">
                        <h3>{titre}</h3>
                        <div style="margin: 20px 0; text-align: center;">
                            <iframe width="100%" height="350" src="{video_url}" frameborder="0" allowfullscreen style="border: 1px solid #39ff14; box-shadow: 0 0 15px rgba(57, 255, 20, 0.2);"></iframe>
                        </div>
                        <p style="white-space: pre-wrap; color: #eee; margin-bottom: 20px;">{description}</p>
                        
                        <div class="exercise-box" style="border-left: 3px solid #39ff14; background: #0a0a0a; padding: 15px; font-family: 'Fira Code', monospace;">
                            <h4 style="color: #39ff14; margin-top: 0;">🎯 TEST_DE_COMPILATION</h4>
                            <p style="color: #ccc;">{question}</p>
                            <ul style="list-style-type: none; padding-left: 0; margin-bottom: 15px;">
                                <li><label><input type="radio" name="q_{quiz_id}" value="A"> <span style="color:#39ff14;">A)</span> {opt_a}</label></li>
                                <li><label><input type="radio" name="q_{quiz_id}" value="B"> <span style="color:#39ff14;">B)</span> {opt_b}</label></li>
                                <li><label><input type="radio" name="q_{quiz_id}" value="C"> <span style="color:#39ff14;">C)</span> {opt_c}</label></li>
                            </ul>
                            
                            <button class="btn-valider" onclick="verifierAuto(this, '{rep}')" style="width:100%;">EXÉCUTER LE CODE</button>
                            
                            <p class="resultat-mini" style="margin-top: 15px; font-weight: bold; font-size: 0.9em; background: #000; padding: 8px; border: 1px solid #222;">
                                <span style="color: #555;">>> status: idle...</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            """
            target.append(BeautifulSoup(nouveau_html, "html.parser"))
            
            with open("dev.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print(f"[+] Module '{titre}' compilé et injecté.")

        elif choix == "2":
            modules = soup.find_all("div", class_="module-container")
            if not modules:
                print("\n[-] Aucun module trouvé.")
                return

            print("\n--- MODULES DEV DISPONIBLES ---")
            liste_titres = [mod.get("data-title") for mod in modules]
            for idx, t in enumerate(liste_titres, 1):
                print(f"{idx}. {t}")

            saisie = input("\nNUMÉRO ou TITRE à supprimer : ")
            if saisie.isdigit():
                index = int(saisie) - 1
                titre_a_suppr = liste_titres[index] if 0 <= index < len(liste_titres) else None
            else:
                titre_a_suppr = saisie

            module = soup.find("div", {"data-title": titre_a_suppr})
            if module:
                module.decompose()
                with open("dev.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
                print(f"[+] Module '{titre_a_suppr}' supprimé.")

    except Exception as e:
        print(f"[-] Erreur : {e}")

if __name__ == "__main__":
    gerer_dev()
