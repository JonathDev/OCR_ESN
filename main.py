from fastapi import FastAPI, HTTPException, Request
from fastapi import Depends

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchimie_module import get_db, recherche_factures, Customer, Invoice

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


# Page d'accueil
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(name="home.html", context={"request": request})

@app.get("/search/")
async def search(
    start_date: str = None, 
    end_date: str = None, 
    name_customer: str = None,
    db: Session = Depends(get_db)
):
    factures = recherche_factures(db, start_date, end_date, name_customer)
    return factures

