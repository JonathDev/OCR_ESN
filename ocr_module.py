from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from msrest.exceptions import HttpOperationError
from dotenv import load_dotenv
import os
import time

def recup_data_feature(url="https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0001-112650.png"):
    try:
        load_dotenv()  # Charge les variables d'environnement

        # Authentification et création du client
        subscription_key = os.environ.get("VISION_KEY")
        endpoint = os.environ.get("VISION_ENDPOINT")

        if not subscription_key or not endpoint:
            return {'statut': 'Erreur', 'message_erreur': 'Clé API ou endpoint non configuré.', 'code_statut': None}

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

        # Appel de l'API avec l'URL et capture directe du code de statut
        read_response = computervision_client.read(url, raw=True)
        
        # Vérifier la réponse initiale
        if read_response.response.status_code != 202:
            return {'statut': 'Erreur', 'message_erreur': 'La requête initiale a échoué.', 'code_statut': read_response.response.status_code}

        # Traitement habituel...
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        # Après traitement, renvoyer le succès et les données extraites
        if read_result.status == OperationStatusCodes.succeeded:
            extracted_data = [{'text': line.text, 'pos': line.bounding_box} for text_result in read_result.analyze_result.read_results for line in text_result.lines]
            return {'statut': 'Succès', 'code_statut': 200 ,'donnees': extracted_data}  # Supposant succès = 200
        else:
            return {'statut': 'Erreur', 'message_erreur': 'Échec de traitement de l\'image.', 'code_statut': None}  # Statut spécifique non disponible ici

    except HttpOperationError as e:
        # Gérer les erreurs spécifiques si possible
        return {'statut': 'Erreur', 'message_erreur': str(e), 'code_statut': e.response.status_code if hasattr(e, 'response') else None}
    except Exception as e:
        # Gérer les exceptions générales
        return {'statut': 'Erreur', 'message_erreur': str(e), 'code_statut': None}

# Exécution et affichage du résultat
#test = recup_data_feature()
#print(test)
