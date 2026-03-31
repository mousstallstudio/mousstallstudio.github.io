import os
from bs4 import BeautifulSoup

def ajouter_cours():
    print("--- MOUSSTALL STUDIO : GÉNÉRATEUR D'AUDIT ---")
    
    # 1. Collecte des infos
    titre = input("Titre du module (ex: SQL INJECTION) : ")
    video_url = input("ID de la vidéo Youtube (ex: PjHqWn0F46A) : ")
    description = input("Petite description du cours : ")
    question = input("Question du Quiz : ")
    reponse_juste = input("La bonne réponse (ex: C) : ")

    # 2. Création du bloc HTML (Template)
    nouveau_cours = f"""
    <button class="accordion">> MODULE : {titre}</button>
    <div class="panel">
        <div class="lesson">
            <h3>{titre}</h3>
            <p>{description}</p>
            <div style="margin: 20px 0; text-align: center;">
                <iframe width="100%" height="350" src="https://www.youtube-nocookie.com/embed/{video_url}" frameborder="0" allowfullscreen style="border: 1px solid #00f2ff;"></iframe>
            </div>
            <div class="exercise-box">
                <h4>🎯 QUIZ RAPIDE</h4>
                <p>{question}</p>
                <p><em>Réponds directement dans ton terminal pour valider ce module.</em></p>
                <p style="color: #00f2ff;">[+] Note : La bonne réponse est {reponse_juste}.</p>
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
            target.append(BeautifulSoup(nouveau_cours, "html.parser"))
            
            with open("audit.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("\n[+] SUCCÈS : Module ajouté à audit.html !")
        else:
            print("[-] ERREUR : ID 'academy-content' non trouvé.")
            
    except FileNotFoundError:
        print("[-] ERREUR : Le fichier audit.html est introuvable.")

if __name__ == "__main__":
    ajouter_cours()
