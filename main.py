from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI(debug=True, title="Udemy FastAPI", version="0.0.0")

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
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
 