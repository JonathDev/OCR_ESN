"""
def cate_phrases(): 
    pattern = r"(.+?)\s+(\d+)\s+x\s+(\d+\.\d+)\s+Euro"
    phrases = traitement_data_facture()
    for phrase in phrases:
        print(phrase)
"""
"""
cate_phrases()
"""
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

"""import re

text = "Rien chaise seconde ciel. 1 x 65.23 Euro"

# Expression régulière pour extraire les informations souhaitées


match = re.search(pattern, text)

if match:
    product_name = match.group(1)
    quantity = match.group(2)
    unit_price = match.group(3)
else:
    product_name, quantity, unit_price = None, None, None

product_name, quantity, unit_price
    """