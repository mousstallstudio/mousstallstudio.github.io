import re

def clean_youtube_link(url):
    # Cette regex est plus agressive pour attraper l'ID de 11 caractères
    # peu importe ce qui vient après (?si=, &t=, etc.)
    regex = r'(?:v=|\/v\/|embed\/|youtu\.be\/|\/shorts\/|^)([a-zA-Z0-9_-]{11})'
    
    match = re.search(regex, url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    return None

def main():
    print("--- MOUSSTALL STUDIO | YT LINK REPAIR ---")
    url_brut = input("Colle ton lien ici : ").strip()
    
    resultat = clean_youtube_link(url_brut)
    
    if resultat:
        print("\n[+] LIEN VALIDE POUR LE BOT D'AUDIT :")
        print(f"👉 {resultat}")
    else:
        print("\n[-] ERREUR : Impossible d'extraire l'ID. Vérifie ton lien.")

if __name__ == "__main__":
    main()
