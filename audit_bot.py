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
    print("\n--- MOUSSTALL STUDIO : GESTIONNAIRE D'AUDIT (V4.0) ---")
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

            sys.stdin = open('/dev/tty') 
            
            question = input("Question Quiz : ")
            opt_a = input("Option A : ")
            opt_b = input("Option B : ")
            opt_c = input("Option C : ")
            rep = input("Bonne réponse (A/B/C) : ").upper()

            quiz_id = titre.replace(" ", "_")

            # --- STRUCTURE AVEC LOG TERMINAL ---
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
                        
                        <div class="exercise-box" style="border-left: 3px solid #00f2ff; background: #0d0d0d; padding: 15px; font-family: 'Courier New', monospace;">
                            <h4 style="color: #00f2ff; margin-top: 0;">🎯 MISSION_QUIZ</h4>
                            <p style="color: #ccc;">{question}</p>
                            <ul style="list-style-type: none; padding-left: 0;">
                                <li><label><input type="radio" name="q_{quiz_id}" value="A"> A) {opt_a}</label></li>
                                <li><label><input type="radio" name="q_{quiz_id}" value="B"> B) {opt_b}</label></li>
                                <li><label><input type="radio" name="q_{quiz_id}" value="C"> C) {opt_c}</label></li>
                            </ul>
                            
                            <button class="btn-valider" 
                                onclick="
                                    let sel = document.querySelector('input[name=\\'q_{quiz_id}\\']:checked')?.value;
                                    let log = document.getElementById('log_{quiz_id}');
                                    if(!sel) {{
                                        log.innerHTML = '<span style=\\'color:#ffcc00\\'>[!] WARNING : No input detected.</span>';
                                    }} else if(sel === '{rep}') {{
                                        log.innerHTML = '<span style=\\'color:#39ff14\\'>[+] SUCCESS : ACCESS_GRANTED.</span>';
                                    }} else {{
                                        log.innerHTML = '<span style=\\'color:#ff003c\\'>[-] ERROR : ACCESS_DENIED.</span>';
                                    }}
                                " 
                                style="background:transparent; color:#00f2ff; border:1px solid #00f2ff; cursor:pointer; padding:8px; width:100%; margin-top:10px; font-weight:bold;">
                                EXECUTER LA VERIFICATION
                            </button>
                            
                            <div id="log_{quiz_id}" style="margin-top: 10px; padding: 5px; background: #000; border: 1px solid #333; min-height: 20px; font-size: 0.9em;">
                                <span style="color: #555;">$ waiting for credentials...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
            target.append(BeautifulSoup(nouveau_html, "html.parser"))
            
            with open("audit.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print(f"[+] Module '{titre}' injecté avec succès (Log Terminal activé).")

        elif choix == "2":
            modules = soup.find_all("div", class_="module-container")
            if not modules:
                print("\n[-] Aucun module trouvé.")
                return

            print("\n--- MODULES D'AUDIT DISPONIBLES ---")
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
                with open("audit.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
                print(f"[+] Module '{titre_a_suppr}' supprimé.")
            else:
                print("[-] Introuvable.")

    except Exception as e:
        print(f"[-] Erreur critique : {e}")

if __name__ == "__main__":
    gerer_audit()
