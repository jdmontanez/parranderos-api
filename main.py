from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from pymongo import MongoClient
from datetime import datetime
import os 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(os.environ["MONGO_URI"])
client = MongoClient("mongodb+srv://jdmontanez:7V0g7LYPVXSk2nk0@fundametosbd.gjmopeo.mongodb.net/?appName=FundametosBD")
db=client["Parranderos"]

@app.get("/")
def inicio():
    return {"message": "Bienvenido a la API de Parranderos!"}

@app.get("/proveedores")
def get_proveedores():
    return list(db["proveedores"].find({}, {"_id": 0}))

@app.get("/proveedores/{bebida_id}")
def get_proveedor_bebida(bebida_id: int):
    proveedor = db["proveedores"].find_one({"bebidas_suministradas": bebida_id}, {"_id": 0})
    return proveedor or {}

@app.post("/proveedores")
def post_proveedor(datos: dict):
    datos["fecha_registro"] = datetime.now().isoformat()
    db["proveedores"].insert_one(datos)
    return {"message": "Proveedor registrado"}

@app.put("/proveedores/{nombre}")
def update_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].replace_one({"nombre": nombre}, datos)
    return {"mensaje": "Proveedor actualizado correctamente"}

@app.patch("/proveedores/{nombre}")
def patch_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].update_one({"nombre": nombre}, {"$set": datos})
    return {"mensaje": "Campos actualizados correctamente"}

@app.delete("/proveedores/{nombre}")
def delete_proveedor(nombre: str):
    resultado = db["proveedores"].delete_one({"nombre": nombre})
    return {"mensaje": f"Proveedor {nombre} eliminado"}