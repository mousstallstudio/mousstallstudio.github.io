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

def gerer_vfx():
    print("\n--- MOUSSTALL STUDIO : GESTIONNAIRE 3D & VFX (V2.1 - Vidéo First) ---")
    print("1. Ajouter un module de rendu")
    print("2. Supprimer un module")
    choix = input("Choix (1/2) : ")

    try:
        if not os.path.exists("3d-vfx.html"):
            print("[-] Erreur : 3d-vfx.html introuvable.")
            return

        with open("3d-vfx.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        target = soup.find(id="academy-content")

        if not target:
            print("[-] Erreur : L'ID 'academy-content' est introuvable.")
            return

        if choix == "1":
            titre = input("Titre du module VFX : ")
            url_brut = input("Lien de la vidéo YouTube : ")
            video_id = extraire_video_id(url_brut)
            
            if not video_id:
                print("[-] ERREUR : Lien YouTube invalide.")
                return

            video_url = f"https://www.youtube.com/embed/{video_id}"
            
            description = saisie_multiligne("Description de la leçon")
            
            # --- PATCH LUBUNTU ---
            sys.stdin = open('/dev/tty') 
            
            question = input("Question Quiz (VFX-Test) : ")
            opt_a = input("Option A : ")
            opt_b = input("Option B : ")
            opt_c = input("Option C : ")
            rep = input("Bonne réponse (A/B/C) : ").upper()

            quiz_id = titre.replace(" ", "_")

            # --- STRUCTURE MODIFIÉE : VIDÉO AVANT TEXTE ---
            nouveau_cours = f"""
            <div class="module-container" data-title="{titre}">
                <button class="accordion" style="border-left: 4px solid #ff003c;">> RENDER_LOG : {titre}</button>
                <div class="panel">
                    <div class="lesson">
                        <h3>{titre}</h3>

                        <div style="margin: 20px 0; text-align: center;">
                            <iframe width="100%" height="350" src="{video_url}" frameborder="0" allowfullscreen style="border: 1px solid #ff003c; box-shadow: 0 0 15px rgba(255, 0, 60, 0.2);"></iframe>
                        </div>

                        <p style="white-space: pre-wrap; color: #eee; margin-bottom: 20px;">{description}</p>
                        
                        <div class="vfx-box" style="border-left: 3px solid #ff003c;">
                            <h4 style="color: #ff003c;">🎯 SHADER_CHALLENGE</h4>
                            <p>{question}</p>
                            <ul style="list-style-type: none; padding-left: 0;">
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="A"> A) {opt_a}</label></li>
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="B"> B) {opt_b}</label></li>
                                <li><label class="quiz-label"><input type="radio" name="q_{quiz_id}" value="C"> C) {opt_c}</label></li>
                            </ul>
                            <button class="btn-valider" style="border-color: #ff003c; color: #ff003c;" onclick="verifierAuto(this, '{rep}')">VÉRIFIER LE RENDU</button>
                            <p class="resultat-mini"></p>
                        </div>
                    </div>
                </div>
            </div>
            """
            target.append(BeautifulSoup(nouveau_cours, "html.parser"))
            print(f"[+] Module VFX '{titre}' compilé dans le pipeline (Format Vidéo-First).")

        elif choix == "2":
            titre_a_suppr = input("Titre du module à supprimer : ")
            module = soup.find("div", {"data-title": titre_a_suppr})
            if module:
                module.decompose()
                print(f"[+] Module '{titre_a_suppr}' retiré.")

        with open("3d-vfx.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    except Exception as e:
        print(f"[-] ERREUR SYSTÈME : {e}")

if __name__ == "__main__":
    gerer_vfx()
