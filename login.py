from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configuración de la conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="nuevo_usuario",
    password="nueva_contrasena",
    database="bdfastapi"
)

# Configurar middleware de sesión
app.add_middleware(SessionMiddleware, secret_key="my_secret_key")

@app.post("/", response_class=HTMLResponse)
async def login(request: Request, usuario: str = Form(...), contrasena: str = Form(...)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuario WHERE usuario = %s AND contrasena = %s", (usuario, contrasena))
    user = cursor.fetchone()

    if user:
        # Guardar el ID del usuario en la sesión
        request.session["idusuario"] = user[0]
        return templates.TemplateResponse("dashboard.html", {"request": request, "usuario_info": user})
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Obtener el ID del usuario de la sesión
    idusuario = request.session.get("idusuario")
    if not idusuario:
        raise HTTPException(status_code=401, detail="No hay sesión activa")

    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id = %s", (idusuario,))
    usuario_info = cursor.fetchone()

    return templates.TemplateResponse("dashboard.html", {"request": request, "usuario_info": usuario_info})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)