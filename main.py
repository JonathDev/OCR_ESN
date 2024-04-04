from fastapi import FastAPI, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchimie_module import get_db, Customer, Invoice, paginate_results, search_invoices
#FAC_2019_0002
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Page d'accueil
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(name="home.html", context={"request": request})

@app.get("/search/", response_class=HTMLResponse)
async def search_form(request: Request):
    # Définir la page par défaut à 1 si non spécifiée
    page = 1
    # Vous pouvez aussi définir une valeur par défaut pour limit ici, si nécessaire
    limit = 10 # Ou une autre valeur par défaut de votre choix
    # Calculer total_pages pour la pagination, même si aucune facture n'est trouvée
    total_pages = 0 # Vous pouvez ajuster cette valeur en fonction de vos besoins
    return templates.TemplateResponse("search.html", {
        "request": request, 
        "page": page, 
        "limit": limit,
        "message": None, # Assurez-vous d'ajouter les autres variables nécessaires
        "factures": [], # Assurez-vous d'envoyer des données vides ou initiales comme nécessaire
        "total_pages": total_pages # Ajoutez total_pages au contexte
    })
@app.post("/search/", response_class=HTMLResponse)
async def search_results(
    request: Request,
    start_date: Optional[str] = Form(None), 
    end_date: Optional[str] = Form(None), 
    name_customer: Optional[str] = Form(None),
    number_invoice: Optional[str] = Form(None), 
    name_product: Optional[str] = Form(None),
    paid: Optional[str] = Form(None), 
    page: int = Query(1, alias="page"), 
    limit: int = Query(10, alias="limit")
):
    try:
        factures = search_invoices(start_date, end_date, name_customer, number_invoice, name_product, paid)
        print(len(factures))
        print(factures)
        page_results, total_pages = paginate_results(factures, page, limit)

    except ValueError:
        page_results, total_pages = [], 0
        # Gestion des exceptions ou logique supplémentaire au besoin

    if not factures:
        message = "Aucune facture correspondant aux critères de recherche n'a été trouvée."
        return templates.TemplateResponse("search.html", {
            "request": request, 
            "message": message, 
            "page": page, 
            "limit": limit, 
            "total_pages": total_pages,
            "factures": factures  # Assurez-vous d'envoyer une liste vide si aucune facture n'est trouvée
        })

    # Retourne la réponse avec tous les factures et variables de pagination nécessaires
    return templates.TemplateResponse("search.html", {
        "request": request, 
        "factures": factures, 
        "page": page, 
        "limit": limit, 
        "total_pages": total_pages
    })
