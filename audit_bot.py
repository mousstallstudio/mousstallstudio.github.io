import os
from bs4 import BeautifulSoup

def gerer_audit():
    print("--- MOUSSTALL STUDIO : GESTIONNAIRE D'AUDIT ---")
    print("1. Ajouter un cours")
    print("2. Supprimer un cours")
    choix = input("Choix (1/2) : ")

    try:
        with open("audit.html", "r", encoding="utf-8") as f:
            content = f.read()
            soup = BeautifulSoup(content, "html.parser")
        
        target = soup.find(id="academy-content")

        if choix == "1":
            titre = input("Titre du module : ")
            video_id = input("ID de la vidéo Youtube (ex: PjHqWn0F46A) : ")
            description = input("Description : ")
            question = input("Question Quiz : ")
            rep = input("Bonne réponse (A/B/C) : ").upper()

            # On utilise youtube-nocookie pour éviter les blocages
            video_url = f"https://www.youtube-nocookie.com/embed/{video_id}"

            # Structure avec 'module-container' pour pouvoir supprimer facilement après
            nouveau_cours = f"""
            <div class="module-container" data-title="{titre}">
                <button class="accordion">> MODULE : {titre}</button>
                <div class="panel">
                    <div class="lesson">
                        <h3>{titre}</h3>
                        <p>{description}</p>
                        <div style="margin: 20px 0; text-align: center;">
                            <iframe width="100%" height="350" src="{video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border: 1px solid #00f2ff;"></iframe>
                        </div>
                        <div class="exercise-box">
                            <h4>🎯 QUIZ</h4>
                            <p>{question}</p>
                            <ul style="list-style-type: none; padding-left: 0;">
                                <li><label><input type="radio" name="q_{video_id}" value="A"> A) Option A</label></li>
                                <li><label><input type="radio" name="q_{video_id}" value="B"> B) Option B</label></li>
                                <li><label><input type="radio" name="q_{video_id}" value="C"> C) Option C</label></li>
                            </ul>
                            <button onclick="verifierAuto(this, '{rep}')" style="background:rgba(0,242,255,0.1); border:1px solid #00f2ff; color:#00f2ff; cursor:pointer; padding:5px 15px; margin-top:10px;">VALIDER</button>
                            <p class="resultat-mini" style="margin-top:10px; font-weight:bold;"></p>
                        </div>
                    </div>
                </div>
            </div>
            """
            target.append(BeautifulSoup(nouveau_cours, "html.parser"))
            print(f"[+] Module '{titre}' ajouté avec succès.")

        elif choix == "2":
            titre_a_suppr = input("Titre du module à supprimer (exact) : ")
            # On cherche la div qui a l'attribut data-title correspondant
            module = soup.find("div", {"data-title": titre_a_suppr})
            
            if module:
                module.decompose()
                print(f"[+] Module '{titre_a_suppr}' supprimé.")
            else:
                print("[-] Erreur : Module introuvable. Vérifie l'orthographe.")

        # Sauvegarde propre
        with open("audit.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    except Exception as e:
        print(f"[-] Erreur système : {e}")

if __name__ == "__main__":
    gerer_audit()
