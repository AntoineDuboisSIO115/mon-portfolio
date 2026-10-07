from datetime import datetime

# 1. Ta liste d'articles validés, rédigés en français et prêts pour le jury
articles_veille = [
    {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "titre": "The Best IDEs and Code Editors for Python (Guide)",
        "lien": "https://realpython.com/python-ides-code-editors-guide/",
        "image": "image/art1.png",
        "source": "Real Python",
        "resume": (
            "Comparatif complet des meilleurs environnements de développement"
            " et éditeurs de code pour Python. L'article analyse les"
            " fonctionnalités clés comme l'autocomplétion, le débogage intégré"
            " et la gestion des environnements virtuels (VS Code, PyCharm,"
            " Neovim). Un choix d'IDE adapté est crucial pour optimiser la"
            " productivité et la maintenabilité du code dans le cadre de nos"
            " projets de développement."
        ),
    },
    # Tu pourras ajouter d'autres articles ici au fil des semaines :
    # {
    #     "date": "14/10/2026",
    #     "titre": "Titre d'un autre article",
    #     "lien": "...",
    #     "image": "image/art2.png",
    #     "source": "Real Python",
    #     "resume": "Mon résumé technique détaillé en français..."
    # }
]

# 2. Lecture du fichier veille.html existant
try:
  with open("veille.html", "r", encoding="utf-8") as f:
    content = f.read()

  articles_ajoutes = 0

  # On parcourt la liste de tes articles
  for article in articles_veille:
    # Vérification anti-doublon : si l'article n'y est pas déjà
    if article["titre"] not in content:
      nouvelle_ligne = f"""
            <tr style="border-bottom: 1px solid var(--border);">
              <td style="padding: 0.75rem 0.5rem; color: var(--text-muted);">{article["date"]}</td>
              <td style="padding: 0.75rem 0.5rem; font-weight: 500;">{article["titre"]}<br>
                <img src="{article["image"]}" alt="Illustration" style="width: 280px; border-radius: 6px; margin-top: 8px; border: 1px solid var(--border);">
              </td>
              <td style="padding: 0.75rem 0.5rem;"><a href="{article["lien"]}" target="_blank" style="color: var(--accent); text-decoration: none;">{article["source"]}</a></td>
              <td style="padding: 0.75rem 0.5rem; color: var(--text-muted);">{article["resume"]}</td>
            </tr>"""

      marker = "<!-- INJECT_HERE -->"
      if marker in content:
        # On insère le nouvel article juste après le repère
        content = content.replace(marker, f"{marker}\n{nouvelle_ligne}")
        articles_ajoutes += 1

  # 3. Enregistrement des modifications si de nouveaux articles ont été ajoutés
  if articles_ajoutes > 0:
    with open("veille.html", "w", encoding="utf-8") as f:
      f.write(content)
    print(
        f"{articles_ajoutes} nouvel(les) article(s) ajouté(s) avec succès !"
    )
  else:
    print("Aucun nouvel article à ajouter.")

except FileNotFoundError:
  print("Erreur : Le fichier veille.html est introuvable.")
