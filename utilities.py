
from QRcode_module import recup_info_data_qrcode
from ocr_module import recup_data_feature
from decimal import Decimal
import re 
from decimal import Decimal, ROUND_HALF_UP



# Exemple de conversion de float en Decimal et utilisation de .quantize
def adjust_decimal(value):
    # Assurez-vous que la valeur est un Decimal avant de quantifier
    adjusted_value = Decimal(value).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    return adjusted_value


    



def processing_data_invoices(url):

    traitements = recup_data_feature(url)
    analyses = traitements['donnees']
    seuil_y = 5
    phrases = []  # Liste pour stocker les phrases complètes
    text = ""  # Initialisation de la variable de texte pour la première ligne
    #print(analyses)
    for i in range(len(analyses) - 1):
        pos_text1 = analyses[i]['pos'][1]  # Position y du coin supérieur gauche de l'élément actuel
        pos_text2 = analyses[i+1]['pos'][1]  # Position y du coin supérieur gauche de l'élément suivant

        if abs(pos_text1 - pos_text2) <= seuil_y:
            # Les éléments sont sur la même ligne
            text += analyses[i]['text'] + " "  # Ajout d'un espace pour séparer les mots
        else:
            # Nouvelle ligne détectée, ajouter le texte actuel à `phrases` et réinitialiser `text`
            text += analyses[i]['text']  # Ajouter le dernier texte de la ligne courante
            phrases.append(text)
            text = ""  # Réinitialisation de `text` pour la nouvelle ligne

    # Ajouter le dernier élément de `analyses` à `text` car il est manqué par la boucle
    text += analyses[-1]['text']
    phrases.append(text)  # Ajouter la dernière phrase compilée à `phrases`
    #print(phrases)
    return phrases



def processing_qrcode_invoices(url):

    resultat =  recup_info_data_qrcode(url)
    return resultat




def sort_data(url):
    sentences_product = []
    pattern_product = r"(?i)(.+?)\s+(\d+)\s+x\s+(\d+\.\d+)\s+Euro"
    #pattern_number_invoice = r"(?i)INVOICE\s+([A-Z_0-9]+)"
    pattern_customer = r"(?i)Bill to\s+([A-Za-z\s\-]+)" 
    pattern_total_price = r"(?i)TOTAL\s+(\d+\.\d+)\s+Euro"
    pattern_adress = r"(?i)^Address\s+(.+)$" 
    #pattern_date_invoice = r"Issue date\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    sentences = processing_data_invoices(url)
    #print(f"dans ma facontion {sentences}")
    infoqcode = processing_qrcode_invoices(url)
    #print(infoqcode)
    for i, sentence in enumerate(sentences):
        if re.match(pattern_product, sentence):
            sentences_product.append(sentence)
        elif re.match(pattern_customer, sentence):
            customer_name = sentence.replace('Bill to ', '') 
            name_customer =  customer_name
            #print(name_customer)
        elif re.match(pattern_total_price, sentence): 
            total_price_modify = sentence
            total_price = total_price_modify.replace("TOTAL", "").replace("Euro", "").strip()
            #print(f"verificationde total_price {total_price}")
            total_price = adjust_decimal(total_price)


            #print(total_price)
        elif re.match(pattern_adress, sentence) :
            adress_modify = sentence + ", " + sentences[i + 1]
            adress = adress_modify.replace('Address ', '')
            #print(adress)


    info_product = {}
    for i, sentence_product in enumerate(sentences_product, start=1):
        match = re.search(pattern_product, sentence_product)
        if match:
            product_name, quantity, unit_price = match.group(1), int(match.group(2)), float(match.group(3))
            # Stocker les informations dans le dictionnaire
            info_product[f'produit{i}'] = {
                'name_product': product_name,
                'quantity': int(quantity),
                "unit_price": adjust_decimal(unit_price)
            }
            #modif_cusomer_id = int(infoqcode.get('CUSTUMER_ID', ''))
     
    invoice_info = {
        'customer_name': name_customer,
        'address': adress,
        'total_price': total_price,
        'products': info_product,
        'url' : url,
        'invoice_number': infoqcode.get('INVOICE', ''),
        'date': infoqcode.get('DATE', ''),
        'customer_id': int(infoqcode.get('CUST', '')),
        'category': infoqcode.get('CAT', ''),
    }
    #print (f" verification des donnée de data_ sort {invoice_info}")
    return invoice_info


