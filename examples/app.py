from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

from fastapi_admin_lite import AdminSite

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="FastAPI Admin Lite Demo")

admin = AdminSite(app, session_factory=SessionLocal, title="Demo Admin")
admin.register_model(User)
admin.mount("/admin")

@app.get("/")
def home():
    return {"message": "FastAPI Admin Lite demo running. Open /admin"}
