from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
import os
from utilities import sort_data
from decimal import Decimal
from datetime import datetime
import pyodbc
import json
import urllib
import traceback


load_dotenv()

# Récupère les variables d'environnement
SERVER = os.getenv('SERVEUR')
ADMIUSER = os.getenv('ADMIUSER')
DATABASE = os.getenv('DATABASE')
PASSWORD = os.getenv('PASSWORD')
DRIVER = os.getenv('DRIVER')
# Informations de connexion (remplacez par vos propres valeurs)
print(SERVER,ADMIUSER,DATABASE,PASSWORD,DRIVER )

# Encode les informations de connexion
#params = urllib.parse.quote_plus(f"DRIVER={DRIVER};SERVER=tcp:{SERVER};DATABASE={DATABASE};UID={ADMIUSER};PWD={PASSWORD};Encrypt=yes;TrustServerCertificate=no;")
#params = urllib3.parse.quote_plus(f"DRIVER={DRIVER};SERVER=tcp:{SERVER};DATABASE={DATABASE};UID={ADMIUSER};PWD={PASSWORD};Encrypt=yes;TrustServerCertificate=no;")
params = urllib.parse.quote_plus(f"DRIVER={DRIVER};SERVER=tcp:{SERVER};DATABASE={DATABASE};UID={ADMIUSER};PWD={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Timeout=200;")





    
# Configuration de votre connexion à la base de données
#conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{SERVEUR}.database.windows.net,1433;Database={DATABASE};Uid={ADMIUSER};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
#connectionString = f'mssql+pyodbc://{ADMIUSER}:{PASSWORD}@{SERVEUR}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server' 

url = "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0002-521208.png" 
#facture = sort_data(url)


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
    unit_price = Column(Numeric)

class Invoice(Base):
    __tablename__ = 'Invoice'
    __table_args__ = {'schema': 'Billing'}
    
    number_invoice = Column(String(50), primary_key=True)
    date_invoice = Column(Date)
    cust_id = Column(Integer, ForeignKey('Billing.Customer.cust_id'))
    total_price = Column(Numeric)
    invoice_link = Column(String)
    
    # Relation à Customer
    customer = relationship("Customer", back_populates="invoices")

class Orders(Base):
    __tablename__ = 'Orders'
    __table_args__ = {'schema': 'Billing'}
    
    order_detail = Column(Integer, primary_key=True)
    number_invoice = Column(String(50), ForeignKey('Invoice.number_invoice'))
    productID = Column(Integer, ForeignKey('product.productID'))
    quantity = Column(Integer)

import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError  # Import specific SQLAlchemy exception

def get_database_engine():
    try:
        # Prepare the connection parameters
        params = urllib.parse.quote_plus(
            "DRIVER={DRIVER};SERVER=tcp:{SERVER};DATABASE={DATABASE};"
            "UID={ADMIUSER};PWD={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Timeout=60;"
            .format(
                DRIVER=os.getenv('DRIVER'), SERVER=os.getenv('SERVER'),
                DATABASE=os.getenv('DATABASE'), ADMIUSER=os.getenv('ADMIUSER'), PASSWORD=os.getenv('PASSWORD')
            )
        )
        
        # Create the engine URL
        engine_url = f"mssql+pyodbc:///?odbc_connect={params}"
        
        # Attempt to create the engine
        engine = create_engine(engine_url, echo=True)
        print("connection réussie")
        
        return engine
    
    except SQLAlchemyError as e:
        # Handle database-related errors
        print(f"Database connection failed: {e}")
        return None
    except Exception as e:
        # Handle other possible errors
        print(f"An error occurred: {e}")
        return None
    
def test_database_connection(engine):
    try:
        # Tente d'obtenir une connexion à la base de données
        with engine.connect() as connection:
            # Exécute une requête simple pour tester la connexion
            result = connection.execute("SELECT GETDATE()")  # Pour SQL Server
            for row in result:
                print(f"Date et heure actuelle du serveur SQL : {row[0]}")
            print("Test de connexion à la base de données réussi.")
    except Exception as e:
        print(f"Erreur lors du test de connexion à la base de données : {e}")


def create_schema_and_tables():
    engine = get_database_engine()
    if engine:
        Base.metadata.create_all(engine)  # Crée toutes les tables définies
        print("Les tables ont été créées avec succès.")
    else:
        print("La création des tables a échoué en raison d'un problème de connexion.")



def get_or_add_customer(session, customer_dict):
    try :
        # Vérifie si le client existe déjà
        existing_customer = session.query(Customer).filter_by(cust_id=int(customer_dict['customer_id'])).first()
        if existing_customer:
            print(f"Client {existing_customer.name_customer} existe déjà.")
            return existing_customer  # Retourne l'objet client existant
        else:
            # Si le client n'existe pas, le créer
            new_customer = Customer(
                cust_id=int(customer_dict['customer_id']),
                name_customer=customer_dict['customer_name'],
                adresse_customer=customer_dict['address'],
                cat=customer_dict['category']
            )
            session.add(new_customer)
            session.commit()
            print(f"Client {customer_dict['customer_name']} ajouté avec succès.")
            return new_customer
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        print(f"c'est dans la session custormer qu'il y a un soucie")
        traceback.print_exc()





def add_product(session, product_dict):
     
    new_product = Product(
    name_product=product_dict['name_product'],
        unit_price=product_dict['unit_price']
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
    finally:
        session.close()


def add_invoice_from_dict(session, invoice_dict, cust_id):
    existing_invoice = session.query(Invoice).filter_by(number_invoice=invoice_dict['invoice_number']).first()
    if not existing_invoice:
        total_price = Decimal(invoice_dict['total_price'])
        invoice_date = datetime.strptime(invoice_dict['date'], '%Y-%m-%d %H:%M:%S')

        new_invoice = Invoice(
            number_invoice=invoice_dict['invoice_number'],
            date_invoice=invoice_date,
            cust_id=cust_id,
            total_price=total_price,
            invoice_link=invoice_dict['url']
        )
        session.add(new_invoice)
        try:
            session.commit()
            print(f"Facture {invoice_dict['invoice_number']} ajoutée avec succès.")
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de l'ajout de la facture : {e}")
    else:
        print(f"Facture {invoice_dict['invoice_number']} existe déjà. Passage à la suivante.")

def get_or_add_product(session, product_dict):
    try : 
        # Vérifie si le produit existe déjà avec le même nom et prix
        existing_product = session.query(Product).filter_by(
            name_product=product_dict['name_product'],
            unit_price=product_dict['unit_price']
        ).first()
        if existing_product:
            print(f"Produit {existing_product.name_product} existe déjà.")
            return existing_product  # Retourne l'objet produit existant
        else:
            # Si le produit n'existe pas, le créer
            new_product = Product(
                name_product=product_dict['name_product'],
                unit_price=product_dict['unit_price']
            )
            session.add(new_product)
            session.commit()
            print(f"Produit {product_dict['name_product']} ajouté avec succès.")
            return new_product
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        # Pour obtenir une trace complète

        traceback.print_exc()    

def add_order(session, number_invoice, productID, quantity):
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



def add(url):
    engine = get_database_engine()
    Session = sessionmaker(bind=engine)
    with Session() as session:

        dict_test = sort_data(url)  # Assurez-vous que cette fonction retourne le format attendu
        #print(dict_test)
        # Ajout du client
       
        customer_dict = {
            'customer_id': dict_test['customer_id'],
            'customer_name': dict_test['customer_name'],
            'address': dict_test['address'],
            'category': dict_test['category']
        }
        print(f"information pour customer : {customer_dict}")
        for key, value in customer_dict.items():
            print(f"Le type de la valeur pour '{key}' est {type(value)}")
        get_or_add_customer(session, customer_dict)
     

        # Ajout de la facture
        invoice_dict = {
            'invoice_number': dict_test['invoice_number'],
            'date': dict_test['date'],
            'total_price': dict_test['total_price'],
            'url': dict_test['url'],
            'customer_id': dict_test['customer_id']
        }
        print(f"information pour facture : {invoice_dict}")

        for key, value in invoice_dict.items():
            print(f"Le type de la valeur pour '{key}' est {type(value)}")
        add_invoice_from_dict(session, invoice_dict, customer_dict['customer_id'])
        

        # Ajout des produits et des commandes
        products_dict = dict_test['products']
        #print(f"information pour produc_dict : {products_dict}")
        for product_info in products_dict.values():
            print(f"information pour produc : {product_info}")
            for key, value in invoice_dict.items():
                print(f"Le type de la valeur pour '{key}' est {type(value)}")
            product_id = get_or_add_product(session, product_info)
            add_order(session, invoice_dict['invoice_number'], product_id, product_info['quantity'])
      
    session.close()

# Assurez-vous d'appeler votre fonction `add(url)` quelque part dans votre script avec l'URL appropriée.
# Utilisez cette fonction juste après avoir créé l'engine pour tester la connexion
engine = get_database_engine()
test_database_connection(engine)
#get_database_engine()
#add(url)