import requests

def recup_data_feactures():
    url = "https://invoiceocrp3.azurewebsites.net/invoices"

    headers = {
        "accept": "application/json"
    }
    all_data = []  # Accumuler les données ici

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        # Si la première requête échoue, renvoyer l'erreur immédiatement
        return {
            'status': 'Erreur',
            'code_statut': response.status_code,
            'erreur': response.reason,
            'donnees': []
        }

    data = response.json().get('invoices', [])
    all_data.extend(data)

    lastDate = data[-1]['dt'] if data else None
    flag = not data  # S'il n'y a pas de données initialement, mettre le drapeau à True

    while not flag:
        urldata = f"https://invoiceocrp3.azurewebsites.net/invoices?start_date={lastDate}"
        responseData = requests.get(urldata, headers=headers)
        
        if responseData.status_code == 200:
            adddata = responseData.json().get('invoices', [])
            if not adddata:
                flag = True
            else:
                all_data.extend(adddata)
                lastDate = adddata[-1]['dt']
        else:
            # S'il y a une erreur dans la boucle, arrêter et retourner ce qui a été accumulé jusqu'à présent avec l'erreur
            return {
                'status': 'Erreur avec requête suivante',
                'code_statut': responseData.status_code,
                'erreur': responseData.reason,
                'donnees': all_data
            }
    
    # Si tout s'est bien passé, retourner les données accumulées
    return {
        'status': 'Succès',
        'code_statut': 200,  # Supposant succès car aucune erreur n'a été rencontrée
        'erreur': None,
        'donnees': all_data
    }

# Exécution de la fonction et affichage du résultat
#test = recup_data_feactures()
#print(test['donnees'])  # Afficher uniquement les données
#print('Nombre de factures récupérées:', len(test['donnees']))
