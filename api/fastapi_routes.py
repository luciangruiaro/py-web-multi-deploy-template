from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from service.hello_service import HelloService
from helpers.utils import format_response


def create_fastapi_app(config):
    app = FastAPI()
    app.state.config = config

    hello_service = HelloService(config)
    templates = Jinja2Templates(directory='templates')
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/hello")
    async def hello_get():
        return JSONResponse(content=format_response("Hello GET", hello_service.say_hello()))

    @app.post("/hello")
    async def hello_post(request: Request):
        data = await request.json()
        return JSONResponse(content=format_response("Hello POST", hello_service.process_data(data)))

    return app
