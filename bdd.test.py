"""
CREATE TABLE operations_log (
    id SERIAL PRIMARY KEY,
    operation_type VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    data_processed TEXT NOT NULL,
    additional_info TEXT
);


CREATE TABLE errors_log (
    id SERIAL PRIMARY KEY,
    operation_id INTEGER NOT NULL,
    error_time TIMESTAMP NOT NULL,
    error_type VARCHAR(255) NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    FOREIGN KEY (operation_id) REFERENCES operations_log (id)
);


CREATE TABLE api_usage_log (
    id SERIAL PRIMARY KEY,
    api_name VARCHAR(255) NOT NULL,
    operation_id INTEGER,
    request_time TIMESTAMP NOT NULL,
    response_status INTEGER NOT NULL,
    data_volume INTEGER,
    FOREIGN KEY (operation_id) REFERENCES operations_log (id)
);
"""
"""


CREATE SCHEMA Billing;

#-- Ensuite, créer les tables dans ce schéma
#-- Notez l'ajout de 'facturation.' devant le nom de chaque table pour spécifier le schéma

CREATE TABLE Billing.Customer (
    cust_id INT PRIMARY KEY,
    adresse_customer TEXT, 
    name_customer TEXT,
    cat VARCHAR(3)
);

CREATE TABLE Billing.Product (
    productID INT PRIMARY KEY,
    name_product TEXT,
    unit_price FLOAT
);

CREATE TABLE Billing.Invoice (
    number_invoice VARCHAR(50) PRIMARY KEY,
    date_invoice DATE,
    cust_id INT,
    invoice_link TEXT,
    total_price FLOAT,
    FOREIGN KEY (cust_id) REFERENCES billing.Customer(cust_id)
);

CREATE TABLE Billing.Orders (
    order_detail INT PRIMARY KEY,
    number_invoice VARCHAR(50),
    productID INT,
    quantity INT,
    FOREIGN KEY (number_invoice) REFERENCES billing.Invoice(number_invoice),
    FOREIGN KEY (productID) REFERENCES billing.Product(productID)


"""

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


load_dotenv()

# Récupère les variables d'environnement
SERVER = os.getenv('SERVEUR')
ADMIUSER = os.getenv('ADMIUSER')
DATABASE = os.getenv('DATABASE')
PASSWORD = os.getenv('PASSWORD')
DRIVER = os.getenv('DRIVER')

conn_str = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:ocr-serveur-jonathan.database.windows.net,1433;Database=db-ocr-jonathan;Uid=ocrjonathan;Pwd=2Alariszera!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
try:
    with pyodbc.connect(conn_str, timeout=10) as conn:
        print("Connexion réussie")
except Exception as e:
    print(f"Erreur lors de la connexion : {e}")