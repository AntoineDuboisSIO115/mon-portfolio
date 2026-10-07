from datetime import datetime
import feedparser

# 1. URL de ton flux RSS
feed_url = "https://realpython.com/atom.xml"
feed = feedparser.parse(feed_url)

if feed.entries:
  # On récupère le tout premier article (le plus récent)
  entry = feed.entries[0]
  titre = entry.title
  lien = entry.link
  date_str = datetime.now().strftime("%d/%m/%Y")

  # Récupération automatique du résumé de l'article depuis le flux RSS (avec un texte de secours si vide)
  resume = (
      entry.get("summary", "")
      .replace("<p>", "")
      .replace("</p>", "")
      .strip()
  )
  if not resume:
    resume = "Nouvelle ressource technique indexée pour la veille."

  # (Optionnel) Tu peux alterner ou choisir une image en fonction du contenu ou d'un compteur
  # Pour l'instant, on garde une structure propre
  image_src = "image/art1.png"

  # 2. Lecture du fichier veille.html existant
  try:
    with open("veille.html", "r", encoding="utf-8") as f:
      content = f.read()

    # Vérification anti-doublon
    if titre in content:
      print(
          "Cet article est déjà présent dans le tableau. Aucune modification"
          " nécessaire."
      )
    else:
      # Construction de la nouvelle ligne HTML
      nouvelle_ligne = f"""
            <tr style="border-bottom: 1px solid var(--border);">
              <td style="padding: 0.75rem 0.5rem; color: var(--text-muted);">{date_str}</td>
              <td style="padding: 0.75rem 0.5rem; font-weight: 500;">{titre}<br>
                <img src="{image_src}" alt="Illustration" style="width: 280px; border-radius: 6px; margin-top: 8px; border: 1px solid var(--border);">
              </td>
              <td style="padding: 0.75rem 0.5rem;"><a href="{lien}" target="_blank" style="color: var(--accent); text-decoration: none;">Real Python</a></td>
              <td style="padding: 0.75rem 0.5rem; color: var(--text-muted);">{resume}</td>
            </tr>"""

      marker = "<!-- INJECT_HERE -->"
      if marker in content:
        updated_content = content.replace(marker, f"{marker}\n{nouvelle_ligne}")

        with open("veille.html", "w", encoding="utf-8") as f:
          f.write(updated_content)
        print(
            "Le tableau de veille a été mis à jour avec le vrai résumé RSS !"
        )
      else:
        print("Erreur : Le repère <!-- INJECT_HERE --> est introuvable.")

  except FileNotFoundError:
    print("Erreur : Le fichier veille.html est introuvable.")
