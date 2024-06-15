# Web-Tool
# Python Web Interaction and Load Testing Tool

## Description

Ce programme Python offre plusieurs fonctionnalités pour interagir avec des serveurs web et des sites web :

1. **Vérifier l'état des serveurs** : Vérifie si un serveur est en ligne et renvoie son code de statut HTTP.
2. **Récupérer le titre d'un site web** : Extrait et affiche le titre de la page HTML d'un site web.
3. **Automatiser les interactions avec un navigateur** : Utilise Selenium pour automatiser des actions sur un site web, comme effectuer une recherche sur Google.
4. **Tester la charge d'un serveur** : Envoie un grand nombre de requêtes HTTP en parallèle à un serveur spécifié pour tester sa résistance.

## Prérequis

- Python 3.x
- [Google Chrome](https://www.google.com/chrome/) et [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (si vous utilisez la fonctionnalité d'automatisation du navigateur)

## Installation des Dépendances

Installez les dépendances nécessaires en utilisant pip :

```bash
pip install requests beautifulsoup4 selenium