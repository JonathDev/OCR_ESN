from factures_module import recup_data_feactures
from sqlalchimie_module import add_fature


def add_invoices():
    data_apis = recup_data_feactures()
    recup_données = data_apis['donnees']
    recup_name_invoices = [data['no'] for data in recup_données]

    print(f"Recupération {recup_name_invoices} et son type est {type(recup_name_invoices)} et sa longueur est {len(recup_name_invoices)}")
    
    urls = [f"https://invoiceocrp3.azurewebsites.net/invoices/{name}" for name in recup_name_invoices]

    factures_problematiques = []

    for url in urls:
        try:
            add_fature(url)
        except Exception as e:
            print(f"Erreur lors de l'ajout de la facture {url}: {e}")
            factures_problematiques.append((url, str(e)))

    return factures_problematiques

add_invoices()


factures_problematiques = add_invoices()

if factures_problematiques:
    print("Les factures suivantes ont rencontré des problèmes et n'ont pas été ajoutées :")
    for facture, erreur in factures_problematiques:
        print(f"- {facture} : {erreur}")
else:
    print("Toutes les factures ont été ajoutées avec succès.")

add_invoices()
    