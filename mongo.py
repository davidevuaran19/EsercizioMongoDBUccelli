import requests
from pymongo import MongoClient

# URL del JSON su GitHub
url = "https://raw.githubusercontent.com/dariusk/corpora/master/data/animals/birds_north_america.json"

try:
    # Effettua una richiesta GET per ottenere il contenuto del file JSON
    response = requests.get(url)
    response.raise_for_status()  # Controlla se ci sono errori HTTP

    # Converte il contenuto della risposta in formato JSON
    data = response.json()
    birds = data.get("birds", [])

    # Connessione al server MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    print("Connessione a MongoDB riuscita!")

    # Nome del database e della collection
    db_name = "uccelli_db"
    collection_name = "uccelli_collection"

    # Accedi o crea il database
    db = client[db_name]

    # Accedi o crea la collection
    if collection_name not in db.list_collection_names():
        print(f"La collection '{collection_name}' non esiste. Verrà creata automaticamente.")
        db.create_collection(collection_name)

    collection = db[collection_name]

    # Inserimento di tutti gli uccelli
    documents = []
    for group in birds:
        family = group.get("family", "Famiglia sconosciuta")
        members = group.get("members", [])
        for member in members:
            documents.append({"name": member, "family": family})

    # Inserisce i documenti nella collection
    if documents:
        result = collection.insert_many(documents)
        print(f"Inseriti {len(result.inserted_ids)} documenti nella collection '{collection_name}'.")

    # Recupero e stampa dei documenti inseriti
    print("Documenti presenti nella collection:")
    for doc in collection.find():
        print(doc)

except requests.exceptions.RequestException as e:
    print(f"Errore durante la richiesta: {e}")
except Exception as e:
    print(f"Errore nella connessione o operazioni con MongoDB: {e}")
