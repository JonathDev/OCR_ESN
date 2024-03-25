
from QRcode_module import recup_info_data_qrcode
from ocr_module import recup_data_feature

class Invoice:
    def __init__(self, number_invoice='', date_invoice='', customer=None, total_price=''):
        self.number_invoice = number_invoice
        self.date_invoice = date_invoice
        self.customer = customer  # Association avec un objet Customer
        self.products = []  # Liste d'associations avec des objets Product
        self.total_price = total_price

class Customer:  
    def __init__(self, customer_name='', address='', cust_id='', cat=''):
        self.cust_id = cust_id = cust_id
        self.customer_name = customer_name
        self.address = address
        self.CAT = cat

class Product:
    def __init__(self, productID="", name_product="", unit_price=""):
        self.productID = productID
        self.name_product = name_product
        self.unit_price = unit_price

class Order: 
    def __init__(self, number_invoice="", product=None, quantity=""):
        self.number_invoice = number_invoice
        self.product = product  # Association avec un objet Product
        self.quantity = quantity



    
    



def traitement_data_facture():

    url = "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0005-1869518.png"
    traitements = recup_data_feature(url)
    analyses = traitements['donnees']
    seuil_y = 5
    phrases = []  # Liste pour stocker les phrases complètes
    text = ""  # Initialisation de la variable de texte pour la première ligne

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

    return phrases



def traitement_qrcode_facture():

    url = "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0005-1869518.png" 
    resultat =  recup_info_data_qrcode(url)
    print(resultat)




def cate_phrases(): 
    phrases = traitement_data_facture()
    print(phrases)


cate_phrases()

"""
    
    # Exemple des positions des blocs de texte
pos_text1 = [37.0, 309.0, 103.0, 310.0, 103.0, 330.0, 37.0, 329.0]
pos_text2 = [546.0, 310.0, 691.0, 311.0, 691.0, 328.0, 546.0, 328.0]

# Extraire les positions y des coins supérieurs pour comparer
y_sup_text1 = pos_text1[1]
y_sup_text2 = pos_text2[1]

# Seuil de différence y pour considérer que les textes sont sur la même ligne
seuil_y = 5.0

# Vérifier si les deux textes sont sur la même ligne
sont_sur_meme_ligne = abs(y_sup_text1 - y_sup_text2) <= seuil_y

# Textes à combiner
text1 = "TOTAL"
text2 = "1661.00 Euro"

# Combinaison des textes si sur la même ligne
if sont_sur_meme_ligne:
    phrase_complete = f"{text1}: {text2}"
else:
    phrase_complete = "Les textes ne sont pas sur la même ligne."

phrase_complete

    """