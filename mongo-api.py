from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
from pydantic import BaseModel
import os

app = FastAPI()

# Permitir conexiones desde APEX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Leer variable de entorno desde Render
MONGO_URI = os.getenv("MONGO_URI")

# Conexión MongoDB
client = MongoClient(MONGO_URI)

# Base de datos
db = client["Admonsis"]


# MODELOS

class Comentario(BaseModel):
    usuario: str
    comentario: str
    calificacion: int


class Evento(BaseModel):
    nombre: str
    descripcion: str
    fecha_evento: str


# RUTAS

@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


# Ruta para probar MongoDB
@app.get("/testmongo")
def testmongo():
    return {
        "colecciones": db.list_collection_names()
    }


# COMENTARIOS

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(
        db["comentarios"].find(
            {"bar_id": bar_id},
            {"_id": 0}
        )
    )
    return comentarios


@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: Comentario):

    nuevo = datos.dict()

    nuevo['bar_id'] = bar_id
    nuevo['fecha'] = datetime.now().isoformat()

    db["comentarios"].insert_one(nuevo)

    return {
        'mensaje': 'Comentario guardado'
    }


# EVENTOS

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):

    eventos = list(
        db["eventos"].find(
            {"bar_id": bar_id},
            {"_id": 0}
        )
    )

    return eventos


@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: Evento):

    nuevo = datos.dict()

    nuevo['bar_id'] = bar_id
    nuevo['fecha_creacion'] = datetime.now().isoformat()

    db["eventos"].insert_one(nuevo)

    return {
        'mensaje': 'Evento guardado'
    }
