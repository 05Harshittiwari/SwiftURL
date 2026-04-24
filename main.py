from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from typing import List
import string
import random

# ---------------- DATABASE SETUP ---------------- #

DATABASE_URL = "sqlite:///./urls.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------- DB MODEL ---------------- #

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True, index=True)
    short_code = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# ---------------- DEPENDENCY ---------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- SCHEMAS ---------------- #

class URLRequest(BaseModel):
    original_url: HttpUrl  # HttpUrl for input validation ✅


class URLResponse(BaseModel):
    original_url: str      # ✅ FIX: use str, not HttpUrl — avoids Pydantic v2 serialization error
    short_url: str
    short_code: str

    class Config:
        from_attributes = True

# ---------------- UTILITY ---------------- #

def generate_short_code(length: int = 6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

# ---------------- APP ---------------- #

app = FastAPI(title="URL Shortener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ---------------- #

@app.post("/shorten", response_model=URLResponse)
def create_short_url(request: URLRequest, db: Session = Depends(get_db)):
    # ✅ FIX: strip trailing slash to avoid duplicates like
    # "https://google.com" and "https://google.com/" being stored separately
    original_url = str(request.original_url).rstrip("/")

    existing = db.query(URL).filter(URL.original_url == original_url).first()
    if existing:
        return {
            "original_url": existing.original_url,
            "short_code": existing.short_code,
            "short_url": f"http://127.0.0.1:8000/{existing.short_code}"
        }

    short_code = generate_short_code()
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "original_url": new_url.original_url,
        "short_code": new_url.short_code,
        "short_url": f"http://127.0.0.1:8000/{new_url.short_code}"
    }


@app.get("/all", response_model=List[URLResponse])
def get_all_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).all()
    return [
        {
            "original_url": url.original_url,
            "short_code": url.short_code,
            "short_url": f"http://127.0.0.1:8000/{url.short_code}"
        }
        for url in urls
    ]


@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url_entry.original_url)


@app.delete("/delete/{short_code}")
def delete_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
    return {"detail": "URL deleted successfully"}