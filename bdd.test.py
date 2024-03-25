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

CREATE TABLE facturation.Product (
    productID INT PRIMARY KEY,
    name_product TEXT,
    unit_price INT
);

CREATE TABLE facturation.Invoice (
    number_invoice VARCHAR(50) PRIMARY KEY,
    date_invoice DATE,
    cust_id INT,
    invoice_link TEXT,
    total_price INT,
    FOREIGN KEY (cust_id) REFERENCES facturation.Customer(cust_id)
);

CREATE TABLE facturation.`Order` (
    order_detail INT PRIMARY KEY,
    number_invoice VARCHAR(50),
    productID INT,
    quantity INT,
    FOREIGN KEY (number_invoice) REFERENCES facturation.Invoice(number_invoice),
    FOREIGN KEY (productID) REFERENCES facturation.Product(productID)


"""