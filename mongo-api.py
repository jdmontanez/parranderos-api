from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

@app.get("/")
def inicio():

    try:

        MONGO_URI = os.getenv("MONGO_URI")

        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        db = client["Admonsis"]

        colecciones = db.list_collection_names()

        return {
            "estado": "conexion exitosa",
            "colecciones": colecciones
        }

    except Exception as e:

        return {
            "error": str(e)
        }
