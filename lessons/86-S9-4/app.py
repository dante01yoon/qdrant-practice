from fastapi import FastAPI
from fastapi.responses import FileResponse

from search import ask_help, client, search_products

app = FastAPI(title="Shop search")


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/search")
def search(q: str, brand: str = "", color: str = ""):
    return search_products(q, brand, color)


@app.get("/ask")
def ask(q: str):
    return ask_help(q)


@app.get("/health")
def health():
    return {name: client.count(name, exact=True).count for name in ["shop", "help"]}
