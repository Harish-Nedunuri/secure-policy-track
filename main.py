import pathlib
import json
import pkg_resources
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from policy_core.SupportUtils.security_utils.auth_routers import router as \
    oauth2_router, router_success, router_refresh, oauth2Scheme
from policy_core.RetrieveTask.router import retrieve_router


with open("package_setup.json", "r") as f:
    package_setup = json.load(f)    
    package_name = package_setup.get("package_name")
version = pkg_resources.get_distribution(package_name).version
BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI(title="Secure Policy Tracker API", version=version,
              description="API for secure retreival of database resources")

# Mount static files
# Setup where your static files are located
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Home Page
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home_view(request: Request):
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
    return templates.TemplateResponse("home.html", {"request": request,"status": "Running!"})

# OAuth2 Authentication/Authorisation Security routers
app.include_router(oauth2_router)
app.include_router(router_refresh)
app.include_router(router_success)

# TODO: Add any Middleware that is appropriate

# Retreive Data
app.include_router(retrieve_router)
