# fastapi-admin-lite

`fastapi-admin-lite` provides a minimal auto-generated admin panel for FastAPI + SQLAlchemy.

## Features (v0.1.0)

- auto CRUD list/delete pages
- HTML admin UI (Jinja2 templates)
- supports SQLAlchemy models
- supports SQLite/Postgres/MySQL
- optional auth dependency hook

## Install

```bash
pip install fastapi-admin-lite
```

## Quick Example

```python
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

from fastapi_admin_lite import AdminSite

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

admin = AdminSite(app, session_factory=SessionLocal)
admin.register_model(User)

admin.mount("/admin")
```

Run:

```bash
uvicorn examples.app:app --reload
```

Open:
http://localhost:8000/admin

## License
MIT
