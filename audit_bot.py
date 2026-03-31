import os
from bs4 import BeautifulSoup

def ajouter_cours():
    print("--- MOUSSTALL STUDIO : GÉNÉRATEUR D'AUDIT ---")
    
    # 1. Collecte des infos
    titre = input("Titre du module (ex: SQL INJECTION) : ")
    video_url = input("ID de la vidéo Youtube (ex: 7S_l4sH_N9E) : ")
    description = input("Petite description du cours : ")
    question = input("Question du Quiz : ")
    reponse_juste = input("La bonne réponse (A, B ou C) : ").upper()

    # 2. Création du bloc HTML interactif
    # On utilise onclick="verifierAuto" qui sera dans le fichier HTML
    nouveau_cours = f"""
    <button class="accordion">> MODULE : {titre}</button>
    <div class="panel">
        <div class="lesson">
            <h3>{titre}</h3>
            <p>{description}</p>
            <div style="margin: 20px 0; text-align: center;">
                <iframe width="100%" height="350" src="https://www.youtube.com/embed/{video_url}" frameborder="0" allowfullscreen style="border: 1px solid #00f2ff;"></iframe>
            </div>
            <div class="exercise-box">
                <h4>🎯 QUIZ INTERACTIF</h4>
                <p>{question}</p>
                <ul style="list-style-type: none; padding-left: 0; line-height: 2;">
                    <li><label style="cursor:pointer"><input type="radio" name="q_{video_url}" value="A"> A) White Hat</label></li>
                    <li><label style="cursor:pointer"><input type="radio" name="q_{video_url}" value="B"> B) Grey Hat</label></li>
                    <li><label style="cursor:pointer"><input type="radio" name="q_{video_url}" value="C"> C) Black Hat</label></li>
                </ul>
                <button onclick="verifierAuto(this, '{reponse_juste}')" style="background: rgba(0, 242, 255, 0.1); border: 1px solid #00f2ff; color: #00f2ff; padding: 5px 15px; cursor: pointer; font-family: 'Fira Code'; margin-top: 10px;">VALIDER LA RÉPONSE</button>
                <p class="resultat-mini" style="margin-top: 10px; font-weight: bold;"></p>
            </div>
        </div>
    </div>
    """

    # 3. Injection dans le fichier HTML
    try:
        with open("audit.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        target = soup.find(id="academy-content")
        if target:
            # On ajoute le nouveau cours
            target.append(BeautifulSoup(nouveau_cours, "html.parser"))
            
            # On sauvegarde avec une belle indentation
            with open("audit.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print(f"\n[+] SUCCÈS : Le module '{titre}' est ajouté !")
        else:
            print("[-] ERREUR : ID 'academy-content' non trouvé.")
            
    except FileNotFoundError:
        print("[-] ERREUR : Le fichier audit.html est introuvable.")

if __name__ == "__main__":
    ajouter_cours()
