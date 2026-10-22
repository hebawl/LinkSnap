from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from psycopg.errors import UniqueViolation
import secrets
import string

from app.db import get_connection

app = FastAPI(title="URL Shortener API")
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length: int = 6) -> str:
    return "".join(
        secrets.choice(ALPHABET)
        for _ in range(length)
    )


class URLRequest(BaseModel):
    url: HttpUrl


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/test-url")
def test_url(request: URLRequest):
    return {
        "received_url": str(request.url),
        "message": "URL received successfully"
    }


@app.post("/links")
def create_link(request: URLRequest):
    original_url = str(request.url)

    for attempt in range(5):
        short_code = generate_short_code()

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO links (short_code, original_url)
                        VALUES (%s, %s)
                        RETURNING id
                        """,
                        (short_code, original_url),
                    )
                    row = cur.fetchone()

            return {
                "id": row[0],
                "short_code": short_code,
                "short_url": f"http://127.0.0.1:8000/{short_code}",
                "original_url": original_url
            }

        except UniqueViolation:
            # A code already exists; generate another one.
            continue

    raise HTTPException(
        status_code=503,
        detail="Could not generate a unique short code. Please try again."
    )


@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT original_url FROM links WHERE short_code = %s",
                (short_code,),
            )
            row = cur.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Short link not found",
        )

    return RedirectResponse(url=row[0], status_code=307)


