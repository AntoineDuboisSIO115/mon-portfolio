from datetime import datetime
from deep_translator import GoogleTranslator
import feedparser

# 1. Liste de tes différents flux RSS de veille
flux_rss = {
    "Real Python": "https://realpython.com/atom.xml",
    "Planet Python": "https://planetpython.org/rss20.xml",
}

# Mots-clés pertinents pour ton orientation
mots_cles_pertinents = [
    "automation",
    "api",
    "script",
    "bot",
    "python",
    "performance",
    "ai",
    "claude",
    "data",
    "tool",
    "compiler",
]

tous_les_articles = []

# 2. Récupération et analyse de tous les flux
for nom_source, url in flux_rss.items():
  feed = feedparser.parse(url)
  for entry in feed.entries:
    titre = entry.title.lower()
    resume_brut = entry.get("summary", "").lower()

    score = 0
    texte_complet = f"{titre} {resume_brut}"
    for mot in mots_cles_pertinents:
      if mot in texte_complet:
        score += 1

    tous_les_articles.append({
        "titre": entry.title,
        "lien": entry.link,
        "source": nom_source,
        "resume": entry.get("summary", "Nouvelle ressource indexée."),
        "score": score,
    })

# Tri pour trouver le plus pertinent
tous_les_articles.sort(key=lambda x: x["score"], reverse=True)

# Lecture du HTML existant
try:
  with open("veille.html", "r", encoding="utf-8") as f:
    content = f.read()
except FileNotFoundError:
  print("Erreur : Le fichier veille.html est introuvable.")
  exit()

# Sélection du meilleur article inédit
article_gagnant = None
for art in tous_les_articles:
  if art["titre"] not in content:
    article_gagnant = art
    break

if article_gagnant:
  titre_original = article_gagnant["titre"]
  lien = article_gagnant["lien"]
  source = article_gagnant["source"]
  date_str = datetime.now().strftime("%d/%m/%Y")

# Nettoyage du résumé brut (suppression des balises HTML basiques)
  resume_brut = (
      article_gagnant["resume"]
      .replace("<p>", "")
      .replace("</p>", "")
      .replace("<br>", " ")
      .strip()
  )

  # TRADUCTION AUTOMATIQUE FORCÉE EN FRANÇAIS
  try:
    titre = GoogleTranslator(source="auto", target="fr").translate(
        titre_original
    )
    print(f"Titre traduit avec succès : {titre}")

    # Traduction explicite du résumé
    resume = GoogleTranslator(source="auto", target="fr").translate(resume_brut)
    print(f"Résumé traduit avec succès : {resume[:50]}...")
  except Exception as e:
    titre = titre_original
    resume = resume_brut
    print(f"Erreur de traduction : {e}")

  if len(resume) > 350:
    resume = resume[:347] + "..."

  image_src = "image/art1.png"

  # 4. Construction de la ligne HTML avec le résumé traduit
  nouvelle_ligne = f"""
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 0.75rem 0.5rem; color: var(--text-muted);">{date_str}</td>
          <td style="padding: 0.75rem 0.5rem; font-weight: 500;">{titre}<br>
            <img src="{image_src}" alt="Illustration" style="width: 280px; border-radius: 6px; margin-top: 8px; border: 1px solid var(--border);">
          </td>
          <td style="padding: 0.75rem 0.5rem;"><a href="{lien}" target="_blank" style="color: var(--accent); text-decoration: none;">{source}</a></td>
          <td style="padding: 0.75rem 0.5rem; color: var(--text-muted);">{resume}</td>
        </tr>"""

  marker = "<!-- INJECT_HERE -->"
  if marker in content:
    updated_content = content.replace(marker, f"{marker}\n{nouvelle_ligne}")

    with open("veille.html", "w", encoding="utf-8") as f:
      f.write(updated_content)
    print(
        f"Succès : Article traduit avec succès et intégré depuis '{source}' !"
    )
  else:
    print("Erreur : Le repère <!-- INJECT_HERE --> est introuvable.")
else:
  print("Aucun nouvel article pertinent trouvé.")
