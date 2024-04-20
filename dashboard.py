from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
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
