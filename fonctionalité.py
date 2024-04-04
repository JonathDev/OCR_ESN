from factures_module import recup_data_feactures
from sqlalchimie_module import add_fature, get_invoice_names
import re


def add_invoices():
    data_apis = recup_data_feactures()
    recup_données = data_apis['donnees']
    recup_name_invoices = [data['no'] for data in recup_données]
    recup_name_invoices_inverse = recup_name_invoices[::-1]

    print(f"Recupération {recup_name_invoices_inverse } et son type est {type(recup_name_invoices_inverse )} et sa longueur est {len(recup_name_invoices_inverse )}")
    
    urls = [f"https://invoiceocrp3.azurewebsites.net/invoices/{name}" for name in recup_name_invoices_inverse]

    factures_problematiques = []

    for url in urls:
        try:
            add_fature(url)
        except Exception as e:
            print(f"Erreur lors de l'ajout de la facture {url}: {e}")
            factures_problematiques.append((url, str(e)))

    return factures_problematiques

"""

factures_problematiques = add_invoices()

if factures_problematiques:
    print("Les factures suivantes ont rencontré des problèmes et n'ont pas été ajoutées :")
    for facture, erreur in factures_problematiques:
        print(f"- {facture} : {erreur}")
else:
    print("Toutes les factures ont été ajoutées avec succès.")
"""
#add_invoices()



def simplify_invoice_name_regex(invoice_name):
    match = re.match(r"([^-]+)", invoice_name)
    if match:
        return match.group(1)
    else:
        return invoice_name  # Retourne le nom original s'il n'y a pas de correspondance

# Exemple d'utilisation
original_name = "FAC_2019_0002-521208"
simplified_name = simplify_invoice_name_regex(original_name)
print(simplified_name)  # Affichera "FAC_2019_0002"

def verif_invoice_and_add():
    data_apis = recup_data_feactures()
    recup_donnees = data_apis['donnees']
    recup_name_invoices = [data['no'] for data in recup_donnees]
    modify_name_invoices = [simplify_invoice_name_regex(data) for data in recup_name_invoices]

    recup_name_invoices_dbb = get_invoice_names()
    
    dif_invoices = []
    for invoice in modify_name_invoices:
        if invoice not in recup_name_invoices_dbb:
            dif_invoices.append(invoice)


    # Pour associer les noms aux identifiants supplémentaires, tu pourrais avoir besoin de mapper les noms modifiés
    # aux noms originaux ou à une autre forme qui contient les identifiants supplémentaires.
    # Cela pourrait être fait par une correspondance directe ou par une recherche dans une structure de données appropriée.

    # Admettons que tu as une fonction ou une méthode pour trouver le nom complet ou l'identifiant supplémentaire
    # basé sur le nom simplifié :
    full_names_or_ids = [find_full_name_or_id(invoice, recup_name_invoices) for invoice in dif_invoices]

    urls = [f"https://invoiceocrp3.azurewebsites.net/invoices/{name}" for name in full_names_or_ids]
    
    factures_problematiques = []

    for url in urls:
        try:
            add_fature(url)
        except Exception as e:
            print(f"Erreur lors de l'ajout de la facture {url}: {e}")
            factures_problematiques.append((url, str(e)))

    return factures_problematiques




def find_full_name_or_id(simplified_name, list_2_full_names):
    for full_name in list_2_full_names:
        if simplified_name in full_name:
            return full_name
    return None
verif_invoice_and_add()