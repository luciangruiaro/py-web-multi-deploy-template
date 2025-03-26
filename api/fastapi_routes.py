from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from api.schemas.hello_schema import HelloRequestModel
from service.hello_service import HelloService
from helpers.utils import format_response


def create_fastapi_app(config):
    app = FastAPI()
    app.state.config = config
    cors_setup(app)

    hello_service = HelloService(config)
    templates = Jinja2Templates(directory='templates')
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/hello")
    async def hello_get():
        try:
            result = hello_service.say_hello()
            return JSONResponse(content=format_response("Hello GET", result))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/hello")
    async def hello_post(data: HelloRequestModel):
        try:
            result = hello_service.process_data(data.dict())
            return JSONResponse(content=format_response("Hello POST", result))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app


def cors_setup(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
