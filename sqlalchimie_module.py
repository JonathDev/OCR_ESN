
import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric, Boolean
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError  # Import specific SQLAlchemy exception
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import Session
import pandas as pd
from contextlib import contextmanager
from dotenv import load_dotenv
import os
from utilities import sort_data
from decimal import Decimal
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import pyodbc
import json
import urllib
import math



logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

load_dotenv()

# Récupère les variables d'environnement
SERVER = os.getenv('SERVEUR')
ADMIUSER = os.getenv('ADMIUSER')
DATABASE = os.getenv('DATABASE')
PASSWORD = os.getenv('PASSWORD')
DRIVER = os.getenv('DRIVER')

conn_str = (
    f"Driver={DRIVER};"
    f"Server=tcp:{SERVER};"
    f"Database={DATABASE};"
    f"Uid={ADMIUSER};"
    f"Pwd={PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Conversion pour SQLAlchemy
connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": urllib.parse.quote_plus(conn_str)}
)

url = 'https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0005-1869518.png'

engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def test_connect():
    try:
        with pyodbc.connect(conn_str, timeout=10) as conn:
            print("Connexion réussie")
            return True
    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
        return False


#url_facture = "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0007-2747871.png" 

# Define your models here
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'Customer'
    __table_args__ = {'schema': 'Billing'}
    
    cust_id = Column(Integer, primary_key=True)
    name_customer = Column(String)
    adresse_customer = Column(String)
    cat = Column(String)
    
    # Relation à Invoice
    invoices = relationship("Invoice", back_populates="customer")

class Product(Base):
    __tablename__ = 'Product'
    __table_args__ = {'schema': 'Billing'}
    
    productID = Column(Integer, primary_key=True)
    name_product = Column(String)
    unit_price = Column(Numeric(10, 2))


class Invoice(Base):
    __tablename__ = 'Invoice'
    __table_args__ = {'schema': 'Billing'}
    
    number_invoice = Column(String(50), primary_key=True)
    date_invoice = Column(Date)
    cust_id = Column(Integer, ForeignKey('Billing.Customer.cust_id'))
    total_price = Column(Numeric(10, 2))
    invoice_link = Column(String)
    # Ajout de la nouvelle colonne pour le statut de paiement
    paid = Column(Boolean, default=False)
    
    # Relation à Customer
    customer = relationship("Customer", back_populates="invoices")

class Orders(Base):
    __tablename__ = 'Orders'
    __table_args__ = {'schema': 'Billing'}
    
    order_detail = Column(Integer, primary_key=True)
    number_invoice = Column(String(50), ForeignKey('Billing.Invoice.number_invoice'))  # Assurez-vous que le schéma est inclus
    productID = Column(Integer, ForeignKey('Billing.Product.productID'))  # Modifier ici en 'Product'
    quantity = Column(Integer)




def create_engine_with_connection_string():
    # Votre chaîne de connexion ODBC
    connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:ocr-serveur-jonathan.database.windows.net;Database=db-ocr-jonathan;Uid=ocrjonathan;Pwd=2Alariszera!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    # Création de l'URL de connexion
    connection_url = URL.create(
        "mssql+pyodbc",
        query={"odbc_connect": connection_string}
    )

    # Création de l'engine
    engine = create_engine(connection_url)
    return engine

def create_schema_and_tables():
    # Votre chaîne de connexion ODBC
    connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:ocr-serveur-jonathan.database.windows.net;Database=db-ocr-jonathan;Uid=ocrjonathan;Pwd=2Alariszera!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

# Création de l'URL de connexion
    connection_url = URL.create(
        "mssql+pyodbc",
        query={"odbc_connect": connection_string}
    )

    # Création de l'engine
    engine = create_engine(connection_url)
    if engine:
        Base.metadata.create_all(engine)  # Crée toutes les tables définies
        print("Les tables ont été créées avec succès.")
    else:
        print("La création des tables a échoué en raison d'un problème de connexion.")




def add_customer_from_dict(session, customer_dict):
        # Vérification si le client existe déjà
    existing_customer = session.query(Customer).filter_by(cust_id=int(customer_dict['customer_id'])).first()
    
    if existing_customer:
        print(f"Le client {customer_dict['customer_name']} existe déjà avec l'ID {customer_dict['customer_id']}. Utilisation du client existant.")
        return existing_customer  # Retourne le client existant
    else:
        new_customer = Customer(
            cust_id=int(customer_dict['customer_id']),  # Assurez-vous que l'ID est un entier
            name_customer=customer_dict['customer_name'],
            adresse_customer=customer_dict['address'],
            cat=customer_dict['category']
        )
        session.add(new_customer)
        try:
            session.commit()
            print(f"Client {customer_dict['customer_name']} ajouté avec succès.")
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de l'ajout du client : {e}")
        finally:
            session.close()
    

def adjust_decimal(value):
    return value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

def add_invoice_from_dict(session, invoice_dict, cust_id):
    # vérification si la facture existe
    existing_invoice = session.query(Invoice).filter_by(number_invoice=invoice_dict['invoice_number']).first()
    
    if existing_invoice:
        print(f"La facture {invoice_dict['invoice_number']} existe déjà. Passage à la suivante.")
        return  # Sortie anticipée de la fonction

    # Convertir la chaîne de prix total en un nombre décimal
    
    adjusted_total_price = adjust_decimal(invoice_dict['total_price'])

    # Convertir la chaîne de date en un objet datetime
    invoice_date = datetime.strptime(invoice_dict['date'], '%Y-%m-%d %H:%M:%S').date()

    new_invoice = Invoice(
        number_invoice=invoice_dict['invoice_number'],
        date_invoice=invoice_date,
        cust_id=cust_id,
        total_price=adjusted_total_price,
        invoice_link=invoice_dict['url']
    )
    session.add(new_invoice)
    try:
        session.commit()
        print(f"Facture {invoice_dict['invoice_number']} ajoutée avec succès.")
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'ajout de la facture : {e}")
    finally:
        session.close()







def add_product(session, product_dict):
    # Convertir unit_price en Decimal pour assurer la correspondance des types de données
    adjusted_unit_price = adjust_decimal(Decimal(product_dict['unit_price']))

    # Recherche d'un produit existant avec le même nom et prix unitaire
    existing_product = session.query(Product).filter_by(
        name_product=product_dict['name_product'], 
        unit_price=adjusted_unit_price
    ).first()
    
    if existing_product:
        print(f"Produit existant {product_dict['name_product']} utilisé.")
        return existing_product.productID  # Retourner l'ID du produit existant pour une utilisation ultérieure
    else:
        new_product = Product(
            name_product=product_dict['name_product'],
            unit_price=adjusted_unit_price  # Utiliser le Decimal converti
        )
        session.add(new_product)
        try:
            session.commit()
            print(f"Produit {product_dict['name_product']} ajouté avec succès.")
            return new_product.productID  # Retourner l'ID du produit pour une utilisation ultérieure
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de l'ajout du produit : {e}")
            return None


    

def add_order(session, number_invoice, productID, quantity):
       # Recherche d'une commande existante avec le même numéro de facture et ID produit
    existing_order = session.query(Orders).filter_by(
        number_invoice=number_invoice, 
        productID=productID
    ).first()
    
    if existing_order:
        print(f"Commande existante pour le produit ID {productID} sous la facture {number_invoice}. Aucune nouvelle commande ajoutée.")
        # Puisque la commande existe déjà, considérez que la facture associée existe aussi, et passez à la suivante
        return
    else :
        new_order = Orders(
            number_invoice=number_invoice,
            productID=productID,
            quantity=quantity
        )
        session.add(new_order)
        try:
            session.commit()
            print(f"Commande pour le produit {productID} ajoutée avec succès.")
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de l'ajout de la commande : {e}")
        finally:
            session.close()

def add_fature(url):
    # Testez la connexion avant de procéder
    if not test_connect():
        print("La connexion a échoué. Vérifiez les informations de connexion.")
        return

    # Créez l'engine si la connexion est réussie
    engine = create_engine_with_connection_string()
    Session = sessionmaker(bind=engine)

    with Session() as session:
        # Récupérez les données à partir de l'URL
        dict_test = sort_data(url)

        # Ajoutez le client
        customer_dict = {
            'customer_id': dict_test['customer_id'],
            'customer_name': dict_test['customer_name'],
            'address': dict_test['address'],
            'category': dict_test['category']
        }
        add_customer_from_dict(session, customer_dict)

        # Ajoutez la facture
        invoice_dict = {
            'invoice_number': dict_test['invoice_number'],
            'date': dict_test['date'],
            'total_price': dict_test['total_price'],
            'url': dict_test['url'],
            'customer_id': dict_test['customer_id']
        }
        add_invoice_from_dict(session, invoice_dict, customer_dict['customer_id'])

        # Ajoutez les produits et les commandes
        products_dict = dict_test['products']
        for product_info in products_dict.values():
            product_id = add_product(session, product_info)
            if product_id is not None:
                add_order(session, invoice_dict['invoice_number'], product_id, product_info['quantity'])

    print("Les données ont été ajoutées avec succès.")


def delete_all_data(session):
    try:
        # Commencez par supprimer les données des tables dépendantes
        session.query(Orders).delete()
        session.query(Invoice).delete()
        session.query(Customer).delete()
        session.query(Product).delete()
        
        # Validez les suppressions
        session.commit()
        print("Toutes les données ont été supprimées avec succès.")
    except Exception as e:
        session.rollback()  # Annulez les modifications en cas d'erreur
        print(f"Erreur lors de la suppression des données : {e}")
    finally:
        session.close()  # Assurez-vous de fermer la session
    
    # Utilisation de la fonction de suppression
def clear_database():
    # Testez la connexion avant de procéder
    if not test_connect():
        print("La connexion a échoué. Vérifiez les informations de connexion.")
        return

    # Créez l'engine si la connexion est réussie
    engine = create_engine_with_connection_string()
    Session = sessionmaker(bind=engine)

    with Session() as session:
        delete_all_data(session)



def get_invoice_names():
    try:
        # Établissement de la session
        engine = create_engine_with_connection_string()
        Session = sessionmaker(bind=engine)
        session = Session()

        # Requête pour récupérer tous les noms des factures
        invoice_names = session.query(Invoice.number_invoice).all()

        # Fermeture de la session
        session.close()

        # Extraction des noms des factures depuis les tuples retournés par la requête
        invoice_names_list = [name[0] for name in invoice_names]
        #print(f"suis dans ma fonction fet : {invoice_names_list}")
        return invoice_names_list
    except Exception as e:
        print(f"Erreur lors de la récupération des noms des factures : {e}")
        return []


# Dans sqlalchimie_module.py
from contextlib import contextmanager

@contextmanager
def get_db():
    print("on vient d'appeler cette fonction")
    db = SessionLocal()
    try:
        print('elle passe par la')
        yield db
    finally:
        
        db.close()
        



def search_invoices(start_date=None, end_date=None, customer_name=None, number_invoice=None, name_product=None, paid=None):
    try:
        # Établissement de la session
        engine = create_engine_with_connection_string()
        Session = sessionmaker(bind=engine)
        session = Session()

        # Construction initiale de la requête
        query = session.query(
            Invoice.number_invoice,
            Invoice.date_invoice,
            Invoice.invoice_link,
            Customer.name_customer,
            Customer.cat,
            Invoice.total_price,
            Product.name_product,
            Orders.quantity,
            Product.unit_price,
            Invoice.paid,# Maintient du statut de paiement
            Customer.adresse_customer
        ).join(Customer, Invoice.cust_id == Customer.cust_id
        ).join(Orders, Orders.number_invoice == Invoice.number_invoice
        ).join(Product, Product.productID == Orders.productID)

        # Ajout de filtres basés sur les paramètres fournis
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Invoice.date_invoice.between(start_date_obj, end_date_obj))
        
        if customer_name:
            query = query.filter(Customer.name_customer == customer_name)
        
        if number_invoice:
            query = query.filter(Invoice.number_invoice == number_invoice)
        
        if name_product:
            query = query.filter(Product.name_product == name_product)

        # Nouveau: Ajout du filtre pour le statut de paiement si spécifié
        if paid is not None:
            # Convertit le paramètre en booléen; True pour 'True', 'true', 1, etc.
            paid_bool = paid.lower() in ['true', '1', 't', 'y', 'yes']
            query = query.filter(Invoice.paid == paid_bool)
        
        # Assurez-vous d'ajouter ORDER BY avant OFFSET et LIMIT
        query = query.order_by(Invoice.date_invoice)

        # Exécution de la requête

        invoices = query.all()

        # Fermeture de la session
        session.close()

        # Traitement des résultats pour regrouper par facture avec détails des produits et le statut de paiement
        invoices_info = {}
        for invoice in invoices:
            invoice_key = invoice[0]  # Numéro de la facture
            if invoice_key not in invoices_info:
                invoices_info[invoice_key] = {
                    'invoice_number': invoice_key,
                    'date_invoice': invoice[1],
                    'invoice_link': invoice[2],
                    'customer_name': invoice[3],
                    'category': invoice[4],
                    'total_price': invoice[5],
                    'paid': invoice[9],  # Inclut l'information de paiement
                    'adresse_customer': invoice[10], 
                    'products': []  # Liste pour stocker les détails des produits
                }
            
            # Ajout de chaque produit dans la liste des produits de la facture correspondante
            invoices_info[invoice_key]['products'].append({
                'product_name': invoice[6],
                'quantity': invoice[7],
                'unit_price': invoice[8]
            })
        
        # Préparation de la sortie en liste de dictionnaires, un par facture
        output = list(invoices_info.values())
        return output
    except Exception as e:
        print(f"Erreur lors de la recherche des factures : {e}")
        return [], 0 



def paginate_results(results, page=1, limit=10):
    start_index = (page - 1) * limit
    end_index = start_index + limit
    page_results = results[start_index:end_index]
    total_pages = math.ceil(len(results) / limit)
    return page_results, total_pages

#test = sort_data('https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0001-112650.png')
#print(test)

def clear_database():
    # Testez la connexion avant de procéder
    if not test_connect():
        print("La connexion a échoué. Vérifiez les informations de connexion.")
        return

    # Créez l'engine si la connexion est réussie
    engine = create_engine_with_connection_string()
    Session = sessionmaker(bind=engine)

    with Session() as session:
        delete_all_data(session)

#clear_database()

def update_invoice(invoice_number, customer_name=None, adresse_customer=None, category=None, total_price=None, paid=None, products=None):
    try:
        # Établissement de la session
        engine = create_engine_with_connection_string()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Recherche de la facture à mettre à jour
        invoice = session.query(Invoice).filter_by(number_invoice=invoice_number).first()
        if invoice is None:
            print(f"Facture {invoice_number} introuvable.")
            return
        
        # Mise à jour des informations de la facture
        invoice.customer.name_customer = customer_name if customer_name else invoice.customer.name_customer
        invoice.customer.adresse_customer = adresse_customer if adresse_customer else invoice.customer.adresse_customer
        invoice.customer.cat = category if category else invoice.customer.cat
        invoice.total_price = total_price if total_price else invoice.total_price
        invoice.paid = paid if paid is not None else invoice.paid

        # Mise à jour des produits associés, si spécifié
        if products:
            for product_info in products:
                product = session.query(Product).filter_by(productID=product_info.get('productID')).first()
                if product:
                    # Mettre à jour les détails du produit existant si nécessaire
                    product.name_product = product_info.get('name_product', product.name_product)
                    product.unit_price = product_info.get('unit_price', product.unit_price)
                    # Trouver ou créer l'association commande-produit
                    order = session.query(Orders).filter_by(productID=product.productID, number_invoice=invoice.number_invoice).first()
                    if order:
                        order.quantity = product_info.get('quantity', order.quantity)
                    else:
                        # Création d'un nouvel ordre si non trouvé
                        new_order = Orders(number_invoice=invoice.number_invoice, productID=product.productID, quantity=product_info.get('quantity'))
                        session.add(new_order)
                else:
                    # Création d'un nouveau produit et d'un nouvel ordre si le produit n'existe pas
                    new_product = Product(productID=product_info.get('productID'), name_product=product_info.get('name_product'), unit_price=product_info.get('unit_price'))
                    session.add(new_product)
                    new_order = Orders(number_invoice=invoice.number_invoice, productID=new_product.productID, quantity=product_info.get('quantity'))
                    session.add(new_order)

        session.commit()
        print(f"Facture {invoice_number} mise à jour avec succès.")
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la mise à jour de la facture : {e}")


def fetch_invoices_data_as_dataframe():
    engine = create_engine_with_connection_string()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Requête pour récupérer les données nécessaires
    invoices_query = session.query(
        Invoice.number_invoice,
        Invoice.date_invoice,
        Invoice.total_price,
        Invoice.paid,
        Customer.name_customer,
        Customer.cat,
        Product.name_product,
        Orders.quantity,
        Product.unit_price
    ).join(Customer, Invoice.cust_id == Customer.cust_id
    ).join(Orders, Orders.number_invoice == Invoice.number_invoice
    ).join(Product, Orders.productID == Product.productID
    ).all()

    # Préparation des données pour le DataFrame
    data = []
    for invoice in invoices_query:
        row = {
            'number_invoice': invoice.number_invoice,
            'date_invoice': invoice.date_invoice,
            'total_price': invoice.total_price,
            'paid': invoice.paid,
            'name_customer': invoice.name_customer,
            'cat': invoice.cat,
            'product_name': invoice.name_product,
            'quantity': invoice.quantity,
            'unit_price': invoice.unit_price
        }
        data.append(row)

    # Création du DataFrame
    df = pd.DataFrame(data)

    # Optionnellement, ajuster le format de la colonne de date et le type de la colonne paid
    df['date_invoice'] = pd.to_datetime(df['date_invoice'])
    df['paid'] = df['paid'].astype(bool)

    session.close()
    print(df)
    return df

