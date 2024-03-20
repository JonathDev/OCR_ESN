import requests

# URL de l'API
url = 'https://invoiceocrp3.azurewebsites.net/invoices'

# Headers de la requête, spécifiant que nous acceptons une réponse en JSON
headers = {
    'accept': 'application/json',
}

# Envoyer la requête GET pour récupérer les métadonnées des images ou leurs URL
response = requests.get(url, headers=headers)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Extraire les données JSON
    images_data = response.json()
    
    # Imprimer les données pour comprendre leur structure
    print(images_data)

    # Continuer le traitement basé sur la structure correcte des données
else:
    # La requête a échoué
    print(f'Échec de la requête : Code d\'état {response.status_code}')

#https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0006.png
