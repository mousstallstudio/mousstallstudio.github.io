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

def gerer_audit():
    print("\n--- MOUSSTALL STUDIO : GESTIONNAIRE D'AUDIT (V3.2) ---")
    print("1. Ajouter un cours")
    print("2. Supprimer un cours")
    choix = input("Choix (1/2) : ")

    try:
        if not os.path.exists("audit.html"):
            print("[-] Erreur : audit.html introuvable.")
            return

        with open("audit.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        target = soup.find(id="academy-content")

        if choix == "1":
            titre = input("Titre du module : ")
            url_brut = input("Lien YouTube : ")
            video_id = extraire_video_id(url_brut)
            
            if not video_id:
                print("[-] Erreur : Lien YouTube invalide.")
                return

            video_url = f"https://www.youtube.com/embed/{video_id}"
            
            description = saisie_multiligne("Description Cyber")

            # RE-OUVERTURE DU FLUX
            sys.stdin = open('/dev/tty') 
            
            question = input("Question Quiz : ")
            opt_a = input("Option A : ")
            opt_b = input("Option B : ")
            opt_c = input("Option C : ")
            rep = input("Bonne réponse (A/B/C) : ").upper()

            quiz_id = titre.replace(" ", "_")

            # --- STRUCTURE MODIFIÉE : VIDÉO AVANT TEXTE ---
            nouveau_html = f"""
            <div class="module-container" data-title="{titre}">
                <button class="accordion" style="border-left: 4px solid #00f2ff;">> AUDIT_LOG : {titre}</button>
                <div class="panel">
                    <div class="lesson">
                        <h3>{titre}</h3>
                        
                        <div style="margin: 20px 0; text-align: center;">
                            <iframe width="100%" height="350" src="{video_url}" frameborder="0" allowfullscreen style="border: 1px solid #00f2ff; box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);"></iframe>
                        </div>

                        <p style="white-space: pre-wrap; color: #eee; margin-bottom: 20px;">{description}</p>
                        
                        <div class="exercise-box" style="border-left: 3px solid #00f2ff; background: rgba(0, 242, 255, 0.05); padding: 15px;">
                            <h4 style="color: #00f2ff;">🎯 MISSION_QUIZ</h4>
                            <p>{question}</p>
                            <ul style="list-style-type: none; padding-left: 0;">
                                <li><label><input type="radio" name="q_{quiz_id}" value="A"> A) {opt_a}</label></li>
                                <li><label><input type="radio" name="q_{quiz_id}" value="B"> B) {opt_b}</label></li>
                                <li><label><input type="radio" name="q_{quiz_id}" value="C"> C) {opt_c}</label></li>
                            </ul>
                            <button class="btn-valider" onclick="alert(document.querySelector('input[name=\\'q_{quiz_id}\\']:checked')?.value === '{rep}' ? '[+] ACCÈS_AUTORISÉ' : '[-] ACCÈS_REFUSÉ')" style="background:transparent; color:#00f2ff; border:1px solid #00f2ff; cursor:pointer; padding:8px; width:100%;">VÉRIFIER L'AUDIT</button>
                        </div>
                    </div>
                </div>
            </div>
            """
            target.append(BeautifulSoup(nouveau_html, "html.parser"))
            
            with open("audit.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            
            print(f"[+] Module '{titre}' injecté avec succès (Format Vidéo-First).")

        elif choix == "2":
            titre_a_suppr = input("Titre à supprimer : ")
            module = soup.find("div", {"data-title": titre_a_suppr})
            if module:
                module.decompose()
                with open("audit.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
                print(f"[+] Module '{titre_a_suppr}' supprimé.")

    except Exception as e:
        print(f"[-] Erreur critique : {e}")

if __name__ == "__main__":
    gerer_audit()
