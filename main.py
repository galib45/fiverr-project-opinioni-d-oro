from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from myapp import app as flask_app
from myapp.models import db

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/home", WSGIMiddleware(flask_app))

@app.get("/")
async def root():
    return RedirectResponse('/home')

@app.get("/api")
async def api_root():
    return {"message": "Hello World"}

@app.route('/robots.txt')
async def robots_txt(request):
    return FileResponse('robots.txt')

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return HTMLResponse("""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <h1 style="font-size: 5em; margin: 0;">404</h1>
            <p style="text-transform: uppercase; font-weight: 600; margin: -0.5em;">
                PAGE NOT FOUND
            </p>
        </div>
    """)
