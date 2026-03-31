#!/bin/bash
clear
echo "🎬 MOUSSTALL ACADEMY - GÉNÉRATEUR AVEC VIDÉO"
echo "----------------------------------------------"

# 1. Sélection de la section
echo "Où ajouter ce cours vidéo ?"
echo "1) AUDIT   2) DEV   3) LE REFLET   4) IA"
read -p "Choix (1-4) : " choice

case $choice in
    1) FILE="audit.html"; COLOR="#00f2ff" ;; # Bleu
    2) FILE="dev.html"; COLOR="#39ff14" ;;   # Vert
    3) FILE="le-reflet.html"; COLOR="#ff003c" ;; # Rouge
    4) FILE="ia.html"; COLOR="#f1c40f" ;;    # Jaune
    *) echo "❌ Erreur"; exit 1 ;;
esac

# 2. Saisie des infos
read -p "👉 Titre (ex: BASES DU RÉSEAU) : " title
read -p "📝 Sous-titre (ex: Modèle OSI) : " lesson_h3
echo "🖋️ Texte court :"
read lesson_p
read -p "🎥 ID YouTube (ex: dQw4w9WgXcQ ou laisser vide) : " vid_id
read -p "💻 Exercice : " exercise

# 3. Préparation du bloc Vidéo (si ID présent)
VIDEO_HTML=""
if [ ! -z "$vid_id" ]; then
    VIDEO_HTML="<div style='margin: 15px 0; border: 1px solid $COLOR;'><iframe width='100%' height='315' src='https://www.youtube.com/embed/$vid_id' frameborder='0' allowfullscreen></iframe></div>"
fi

# 4. Construction du bloc HTML final
NEW_BLOCK="<button class='accordion'>> $title</button>\n<div class='panel'>\n  <div class='lesson'>\n    <h3>$lesson_h3</h3>\n    <p>$lesson_p</p>\n    $VIDEO_HTML\n    <div class='exercise-box' style='border-left: 3px solid $COLOR; padding: 10px; background: rgba(0,0,0,0.3);'><strong>🛠️ EXERCICE :</strong> $exercise</div>\n  </div>\n</div>"

# 5. Injection (avant le lien de retour)
sed -i "/class=\"back-link\"/i $NEW_BLOCK" $FILE

echo "----------------------------------------------"
echo "✅ Cours avec vidéo ajouté dans $FILE !"

# 6. Publication
read -p "🚀 Publier sur GitHub ? (o/n) : " publish
if [ "$publish" = "o" ]; then
    git add .
    git commit -m "Nouveau cours vidéo : $lesson_h3"
    git push origin main
fi
