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


        /* Mise en forme du conteneur principal */
        .carte_visite_recto_verso {
            flex: 0 0 auto;
            width: calc(25% - 40px); /* 20% pour 4 par ligne et 20px pour compter les marges des deux côtés */
            margin: 20px;
            -webkit-perspective: 800px;
            perspective: 800px;
            position: relative;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2)
        }

     /* Mise en forme générale de la carte (taille et préservation de la position 3D des objets fils) */
     .carte_visite_recto_verso .carte {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        position: absolute;
        backface-visibility: hidden;
        -webkit-transform-style: preserve-3d;
        transform-style: preserve-3d;
        transition: transform 0.5s; /* Ajout d'une transition pour une animation fluide */
    }

        /* Principe général des couches : non affichée en mode retourné */
        .carte_visite_recto_verso .carte .couche {
            margin: 0px !important;
            -webkit-transition: 0.5s;
            transition: 0.5s;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
        }

        /* Positionnement du recto à l'intérieur du bloc carte */
        .carte_visite_recto_verso .carte .recto {
            width: 100%; /* A adapter à votre besoin */
            height: 420px; /* A adapter à votre besoin */
            position: absolute;
            z-index: 1;
        }

 
        /* Rotation initiale des couches dont la couche verso est retournée (-180) pour la rendre invisible */
        .carte_visite_recto_verso .carte .verso {
            transform: rotateY(-180deg);
            position: absolute;
            top: 0;
        }

        /* Rotation pour montrer le verso de la carte */
        .carte_visite_recto_verso .carteModeVerso .recto {
            transform: rotateY(180deg);
        }

        /* Rotation pour montrer le recto de la carte */
        .carte_visite_recto_verso .carteModeVerso .verso {
            transform: rotateY(0deg);
        }

   




/* Mise en forme de la pagination */
.pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
.pagination a {
    margin: 0 5px;
    padding: 5px 10px;
    border: 1px solid #ddd;
    text-decoration: none;
    color: #333;
}
.pagination a.active {
    background-color: #007bff;
    color: white;
}
