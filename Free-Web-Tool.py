import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys

url = "http://127.0.0.1:8080"

# Fonction pour envoyer une requête au serveur
def access_server():
    try:
        response = requests.get(url)
        return f"Réponse du serveur: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la requête: {e}"

# Fonction pour afficher une barre de progression
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()

# Nombre de requêtes
nombre_acces = 10000  # Limité pour la version gratuite

# Utilisation de ThreadPoolExecutor pour exécuter des requêtes en parallèle
max_workers = 100

print("Lancement de l'attaque (version gratuite)...\n")

try:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(access_server) for _ in range(nombre_acces)]

        for i, future in enumerate(as_completed(futures)):
            print_progress_bar(i + 1, nombre_acces, prefix='Progress:', suffix='Complete', length=50)
            result = future.result()
            sys.stdout.write(f'\r{result}')
            sys.stdout.flush()
except KeyboardInterrupt:
    print("\nTest interrompu par l'utilisateur.")