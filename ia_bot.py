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
    print("(Collez votre texte, puis faites ENTREE + CTRL+D pour valider)")
    print("-" * 30)
    contenu = sys.stdin.read()
    print("-" * 30)
    return contenu.strip()

def gerer_ia():
    print("\n--- MOUSSTALL STUDIO : GESTIONNAIRE IA (V2.1 - Vidéo First) ---")
    print("1. Ajouter un module de recherche")
    print("2. Supprimer un module")
    choix = input("Choix (1/2) : ")

    try:
        if not os.path.exists("ia.html"):
            print("[-] Erreur : ia.html introuvable.")
            return

        with open("ia.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        target = soup.find(id="academy-content")

        if choix == "1":
            titre = input("Titre du module IA : ")
            url_brut = input("Lien YouTube : ")
            video_id = extraire_video_id(url_brut)
            
            if not video_id:
                print("[-] ID YouTube introuvable.")
                return

            video_url = f"https://www.youtube.com/embed/{video_id}"
            
            desc = saisie_multiligne("Description du module IA")
            
            # Ré-ouverture du flux clavier pour Lubuntu
            sys.stdin = open('/dev/tty') 
            
            ques = input("Question Quiz (AI-Logic) : ")
            opt_a = input("A : ")
            opt_b = input("B : ")
            opt_c = input("C : ")
            rep = input("Réponse (A/B/C) : ").upper()

            quiz_id = titre.replace(" ", "_")

            # --- STRUCTURE MODIFIÉE : VIDÉO AVANT TEXTE ---
            nouveau_cours = f"""
            <div class="module-container" data-title="{titre}">
                <button class="accordion" style="border-left: 4px solid #f1c40f;">> AI_LOG : {titre}</button>
                <div class="panel">
                    <div class="lesson">
                        <h3>{titre}</h3>

                        <div style="margin: 20px 0; text-align: center;">
                            <iframe width="100%" height="350" src="{video_url}" frameborder="0" allowfullscreen style="border: 1px solid #f1c40f; box-shadow: 0 0 15px rgba(241, 196, 15, 0.2);"></iframe>
                        </div>

                        <p style="white-space: pre-wrap; color: #eee; margin-bottom: 20px;">{desc}</p>
                        
                        <div class="lab-note" style="border-left: 3px solid #f1c40f;">
                            <h4 style="color: #f1c40f;">🧠 NEURAL_TEST</h4>
                            <p>{ques}</p>
                            <ul style="list-style-type: none; padding-left: 0;">
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="A"> A) {opt_a}</label></li>
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="B"> B) {opt_b}</label></li>
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="C) {opt_c}</label></li>
                            </ul>
                            <button class="btn-valider" style="border-color: #f1c40f; color: #f1c40f;" onclick="verifierAuto(this, '{rep}')">EXECUTER L'ANALYSE</button>
                            <p class="resultat-mini"></p>
                        </div>
                    </div>
                </div>
            </div>
            """
            target.append(BeautifulSoup(nouveau_cours, "html.parser"))
            print(f"[+] Module IA '{titre}' synchronisé (Format Vidéo-First).")

        elif choix == "2":
            titre_a_suppr = input("Titre à supprimer : ")
            module = soup.find("div", {"data-title": titre_a_suppr})
            if module:
                module.decompose()
                print(f"[+] Module '{titre_a_suppr}' déconnecté.")

        with open("ia.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    except Exception as e:
        print(f"[-] Erreur : {e}")

if __name__ == "__main__":
    gerer_ia()
