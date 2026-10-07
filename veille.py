from datetime import datetime
import feedparser

# 1. URL de ton flux RSS
feed_url = "https://realpython.com/atom.xml"
feed = feedparser.parse(feed_url)

if feed.entries:
  # On prend le dernier article du flux
  entry = feed.entries[0]
  titre = entry.title
  lien = entry.link
  date_str = datetime.now().strftime("%d/%m/%Y")

  resume = (
      "Analyse automatique du flux RSS : nouveauté technique détectée et"
      " intégrée pour la veille."
  )

  # 2. Lecture du fichier veille.html existant
  try:
    with open("veille.html", "r", encoding="utf-8") as f:
      content = f.read()

    # Vérification anti-doublon : si le titre y est déjà, on ne fait rien
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
                <img src="image/art1.png" alt="Illustration" style="width: 280px; border-radius: 6px; margin-top: 8px; border: 1px solid var(--border);">
              </td>
              <td style="padding: 0.75rem 0.5rem;"><a href="{lien}" target="_blank" style="color: var(--accent); text-decoration: none;">Real Python</a></td>
              <td style="padding: 0.75rem 0.5rem; color: var(--text-muted);">{resume}</td>
            </tr>"""

      marker = "<!-- INJECT_HERE -->"
      if marker in content:
        updated_content = content.replace(marker, f"{marker}\n{nouvelle_ligne}")

        with open("veille.html", "w", encoding="utf-8") as f:
          f.write(updated_content)
        print("Le tableau de veille a été mis à jour avec succès !")
      else:
        print("Erreur : Le repère <!-- INJECT_HERE --> est introuvable.")

  except FileNotFoundError:
    print("Erreur : Le fichier veille.html est introuvable.")
