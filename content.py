from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Aquí puedes agregar la lógica para obtener los datos del usuario u otras operaciones necesarias
    usuario_info = {"nombre": "Usuario de ejemplo", "rol": "Admin"}

    # Renderiza el template "dashboard.html" con los datos del usuario
    return templates.TemplateResponse("dashboard.html", {"request": request, "usuario_info": usuario_info})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
