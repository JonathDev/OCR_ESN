import matplotlib.pyplot as plt
import pandas as pd
from sqlalchimie_module import fetch_invoices_data_as_dataframe
import matplotlib.ticker as ticker


def generate_revenue_chart():
    df = fetch_invoices_data_as_dataframe()
    df['year'] = pd.to_datetime(df['date_invoice']).dt.year
    revenue_per_year = df.groupby('year')['total_price'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(revenue_per_year['year'].astype(str), revenue_per_year['total_price'], color='skyblue')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Revenue')
    ax.set_title('Annual Revenue')
    plt.xticks(rotation=45)

    # Formater les étiquettes de l'axe des ordonnées pour inclure le symbole de l'euro (€)
    # et afficher les nombres avec deux chiffres après la virgule
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('€%0.2f'))

    # Afficher les valeurs des revenus sur chaque barre
    for bar in bars:
        height = bar.get_height()
        ax.annotate('€{:.2f}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # Décalage vertical pour le texte
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('static/revenue_chart.png', format='png')
    plt.close()


def camenber_top10_customer(): 
    # Supposons que df soit votre DataFrame contenant les données des factures
  df = fetch_invoices_data_as_dataframe()

  # Grouper par 'name_customer' et calculer le total des achats pour chaque client
  total_per_customer = df.groupby('name_customer')['total_price'].sum().sort_values(ascending=False)

  # Sélectionner les dix plus grands clients
  top_ten_customers = total_per_customer.head(10)

  # Convertir en DataFrame pour faciliter le tracé
  top_ten_customers_df = top_ten_customers.reset_index()
  
  # Création du diagramme circulaire
  plt.figure(figsize=(10, 8))
  plt.pie(top_ten_customers_df['total_price'], labels=top_ten_customers_df['name_customer'], autopct='%1.1f%%', startangle=140)
  plt.title('Top 10 Clients par Total des Achats')
  plt.axis('equal')  # Assurez que le pie chart est un cercle

  # Sauvegarder le diagramme dans un fichier
  plt.savefig('static/top_ten_customers_pie_chart.png')
  plt.close()



def generate_customer_revenue_chart():
    df = fetch_invoices_data_as_dataframe()

    # Grouper par 'name_customer' et calculer le total des achats pour chaque client
    total_per_customer = df.groupby('name_customer')['total_price'].sum().sort_values(ascending=False)

    # Pour limiter le nombre de clients affichés, vous pouvez utiliser .head(n) pour n clients
    # Sinon, cela affichera tous les clients
    top_customers = total_per_customer.head(20)  # Exemple pour les 20 plus grands clients

    fig, ax = plt.subplots(figsize=(14, 8))  # Ajustez la taille au besoin
    bars = ax.bar(top_customers.index, top_customers.values, color='skyblue')
    ax.set_xlabel('Customer Name')
    ax.set_ylabel('Total Revenue')
    ax.set_title('Total Revenue by Customer')
    plt.xticks(rotation=90)  # Rotation pour une meilleure lisibilité des noms des clients

    # Formater les étiquettes de l'axe des ordonnées pour inclure le symbole de l'euro (€)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('€%0.2f'))

    plt.tight_layout()
    plt.savefig('static/customer_revenue_chart.png', format='png')
    plt.close()


def top_revenue_products():
    df = fetch_invoices_data_as_dataframe()

    # Calculer le revenu total pour chaque ligne
    df['total_revenue'] = df['quantity'] * df['unit_price']

    # Grouper par 'product_name' et calculer le revenu total pour chaque produit
    total_revenue_per_product = df.groupby('product_name')['total_revenue'].sum().sort_values(ascending=False)

    # Sélectionner les dix produits générant le plus de revenus
    top_ten_revenue_products = total_revenue_per_product.head(10)

    # Préparer les données pour le tracé
    top_ten_revenue_products_df = df[df['product_name'].isin(top_ten_revenue_products.index)].drop_duplicates(subset='product_name')

    # Tracer
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.bar(top_ten_revenue_products.index, top_ten_revenue_products.values, color='skyblue')

    # Ajouter les étiquettes des revenus totaux sur les barres
    for bar, revenue in zip(bars, top_ten_revenue_products.values):
        ax.text(bar.get_x() + bar.get_width() / 2, revenue, f'€{revenue:.2f}',
                ha='center', va='bottom')

    ax.set_xlabel('Product Name')
    ax.set_ylabel('Total Revenue')
    ax.set_title('Top 10 Products by Revenue')
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig('static/top_ten_revenue_products_chart.png')
    plt.close()


def bottom_revenue_products():
    df = fetch_invoices_data_as_dataframe()

    # Calculer le revenu total pour chaque ligne
    df['total_revenue'] = df['quantity'] * df['unit_price']

    # Grouper par 'product_name' et calculer le revenu total pour chaque produit
    total_revenue_per_product = df.groupby('product_name')['total_revenue'].sum().sort_values(ascending=True)

    # Sélectionner les dix produits générant le moins de revenus
    bottom_ten_revenue_products = total_revenue_per_product.head(10)

    # Préparer les données pour le tracé
    bottom_ten_revenue_products_df = df[df['product_name'].isin(bottom_ten_revenue_products.index)].drop_duplicates(subset='product_name')

    # Tracer
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.bar(bottom_ten_revenue_products.index, bottom_ten_revenue_products.values, color='skyblue')

    # Ajouter les étiquettes des revenus totaux sur les barres
    for bar, revenue in zip(bars, bottom_ten_revenue_products.values):
        ax.text(bar.get_x() + bar.get_width() / 2, revenue, f'€{revenue:.2f}',
                ha='center', va='bottom')

    ax.set_xlabel('Product Name')
    ax.set_ylabel('Total Revenue')
    ax.set_title('Bottom 10 Products by Revenue')
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig('static/bottom_ten_revenue_products_chart.png')
    plt.close()
    
def camenber_bottom10_customer(): 
    df = fetch_invoices_data_as_dataframe()

    total_per_customer = df.groupby('name_customer')['total_price'].sum().sort_values(ascending=True)
    bottom_ten_customers = total_per_customer.head(10)
    bottom_ten_customers_df = bottom_ten_customers.reset_index()
  
    plt.figure(figsize=(10, 8))

    # Création du diagramme circulaire avec une fonction personnalisée pour autopct
    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '€{v:d}\n({p:.1f}%)'.format(v=val,p=pct)
        return my_format
    
    plt.pie(bottom_ten_customers_df['total_price'], labels=bottom_ten_customers_df['name_customer'], autopct=autopct_format(bottom_ten_customers_df['total_price']), startangle=140)
    plt.title('Bottom 10 Clients par Total des Achats')
    plt.axis('equal')

    plt.savefig('static/bottom_ten_customers_pie_chart.png')
    plt.close()