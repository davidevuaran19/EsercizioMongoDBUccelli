#Cosa deve fare il programma? recuperare dei dati da json e connettersi al db mongodb, creare collection. trasportare da json a mongodb

import requests
import json

# URL del sito da cui recuperare il JSON
url = "https://jsonplaceholder.typicode.com/posts"  # Usa l'URL appropriato

try:
    # Effettua una richiesta GET
    response = requests.get(url)
    response.raise_for_status()  # Controlla se ci sono errori HTTP

    # Converte il contenuto della risposta in formato JSON
    data = response.json()

    # Itera sugli oggetti del JSON
    for obj in data:
        print(f"ID: {obj['id']}, Titolo: {obj['title']}")

except requests.exceptions.RequestException as e:
    print(f"Errore durante la richiesta: {e}")
except json.JSONDecodeError:
    print("Errore nel parsing del JSON")
