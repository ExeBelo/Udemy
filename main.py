
from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel


class User(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str
    edad: int

class Curso(BaseModel):
    titulo: str
    descripcion: str
    duracion: int
    instructor: str
    

app = FastAPI(debug=True, title="Udemy FastAPI", version="0.0.1")

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.get("/")
def defecto():
    return {"mensaje": "Bienvenido a la API de Udemy"}

@app.get("/usuarios")
def get_usuarios():
    usuarios = db.collection("usuarios")
    lista_usuarios = [doc.to_dict() for doc in usuarios.stream()]
    return lista_usuarios
@app.get("/cursos")
def get_cursos():
    cursos = db.collection("cursos")
    lista_cursos = [doc.to_dict() for doc in cursos.stream()]
    return lista_cursos

@app.post("/usuarios")
def add_user(data: User):
    db.collection("usuarios").add(data.dict())
    return {"mensaje": "Usuario agregado correctamente"}
 
@app.post("/cursos")
def add_user(data: Curso):
    db.collection("cursos").add(data.dict())
    return {"mensaje": "curso agregado correctamente"}

@app.post("/login")
def login(email: str, password: str): # aca le pido los parametros para el login
    usuarios = db.collection("usuarios") #aca agarro la tabla
    usuario = usuarios.where("email", "==", email).where("password", "==", password).stream() #aca hago la consulta
    for usuarios in usuario: #si encontro algo scofield jaj
        return {"mensaje": "Login exitoso, bienvenido " + usuarios.to_dict()["nombre"] + " " + usuarios.to_dict()["apellido"]}
    return {"mensaje": "Credenciales incorrectas"} # si no encontro nada

@app.post("/register") #para que  no sea lo mismo que el post usuarios, le pusimos que verifique que el email no este registrado y sin usar la clase User
def register(nombre: str, apellido: str, email: str, password: str, edad: int):
    usuarios = db.collection("usuarios")
    usuario = usuarios.where("email", "==", email).stream()
    for usuarios in usuario:
        return {"mensaje": "El email ya está registrado"}
    db.collection("usuarios").add({
    "nombre": nombre, 
    "apellido": apellido,
    "email": email, 
    "password": password,
    "edad": edad })
    return {"mensaje": "Usuario registrado correctamente"}

