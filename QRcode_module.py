import requests
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode

def recup_info_data_qrcode(url='https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0002-521208.png'):
    try:
        # Obtenir l'image depuis l'URL
        response = requests.get(url)
        # S'assurer que la requête a réussi
        response.raise_for_status()  # Ceci va lever une exception si le statut n'est pas 200

        # Charger l'image obtenue
        image = Image.open(BytesIO(response.content))

        # Décoder le QR Code
        decoded_objects = decode(image)

        if decoded_objects:
            # Supposant un seul QR Code dans l'image, on prend le premier objet décodé
            obj = decoded_objects[0]
            type_data = obj.type
            donnee_data = obj.data.decode('utf-8')
            
            # Séparer les données décodées en utilisant le retour à la ligne comme séparateur
            donnees_separees = donnee_data.split('\n')
            donnees_dict = {'Type': type_data}
            for donnee in donnees_separees:
                cle, valeur = donnee.split(':', 1)  # Diviser chaque ligne en clé et valeur
                donnees_dict[cle] = valeur  # Ajouter au dictionnaire
            
            donnees_dict['statut'] =  "Aucun probleme"
            donnees_dict['Statut Réponse'] = response.status_code  # Ajouter le statut de la réponse
            
            return donnees_dict
        else:
            return {"statut": "Aucun QR Code détecté dans l'image.", 'Statut Réponse': response.status_code}

    except requests.exceptions.RequestException as e:
        # Retourner l'erreur liée aux requêtes HTTP
        return {"statut": f"Erreur lors de la récupération de l'image: {e}", 'Statut Réponse': None}
    except IOError as e:
        # Retourner l'erreur d'ouverture de l'image
        return {"statut": f"Erreur lors de l'ouverture de l'image: {e}", 'Statut Réponse': response.status_code if 'response' in locals() else None}
    except Exception as e:
        # Retourner toute autre erreur inattendue
        return {"statut": f"Une erreur inattendue est survenue: {e}", 'Statut Réponse': response.status_code if 'response' in locals() else None}


#test = recup_info_data_qrcode()
#print(test)