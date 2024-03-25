from QRcode_module import recup_info_data_qrcode
from factures_module import recup_data_feactures
from ocr_module import recup_data_feature



def main():
    resultat = recup_data_feactures()
    resultat_name_statut = resultat['status']
    resultat_name_code_statut = resultat['code_statut']

    if resultat['status'] == 'Succès':  # Assurez-vous que la récupération a réussi
        factures = resultat['donnees']  # Obtenez la liste des factures
        names_factures = [facture.get('no') for facture in factures]  # Récupérer les numéros de toutes les factures

    #print(resultat_name_statut, resultat_name_code_statut, names_factures, type(names_factures))

    for name in names_factures: 
        #print(name)
        url = f"https://invoiceocrp3.azurewebsites.net/invoices/{name}"
        data_factures = recup_data_feature(url)
        data_qrcode_factures= recup_info_data_qrcode(url)
        #print(data_factures)
        #print(data_qrcode_factures)
        print(url)


main()