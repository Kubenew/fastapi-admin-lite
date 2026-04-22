from typing import Callable, List, Type, Optional

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


class AdminSite:
    def __init__(
        self,
        app: FastAPI,
        session_factory: Callable[[], Session],
        title: str = "Admin Lite",
        auth_dependency: Optional[Callable] = None,
    ):
        self.app = app
        self.session_factory = session_factory
        self.title = title
        self.auth_dependency = auth_dependency
        self.models: List[Type] = []

        self.templates = Jinja2Templates(directory=self._template_dir())

    def _template_dir(self) -> str:
        import os
        return os.path.join(os.path.dirname(__file__), "templates")

    def register_model(self, model: Type):
        self.models.append(model)

    def mount(self, prefix: str = "/admin"):
        @self.app.get(prefix, response_class=HTMLResponse)
        def admin_index(request: Request, _=Depends(self.auth_dependency) if self.auth_dependency else None):
            return self.templates.TemplateResponse(
                "index.html",
                {"request": request, "title": self.title, "models": self.models, "prefix": prefix},
            )

        @self.app.get(prefix + "/{model_name}", response_class=HTMLResponse)
        def list_model(model_name: str, request: Request, _=Depends(self.auth_dependency) if self.auth_dependency else None):
            model = self._get_model(model_name)
            if not model:
                return HTMLResponse("Model not found", status_code=404)

            db = self.session_factory()
            try:
                items = db.query(model).all()
            finally:
                db.close()

            cols = [c.name for c in model.__table__.columns]

            return self.templates.TemplateResponse(
                "list.html",
                {
                    "request": request,
                    "title": self.title,
                    "model_name": model_name,
                    "items": items,
                    "cols": cols,
                    "prefix": prefix,
                },
            )

        @self.app.get(prefix + "/{model_name}/delete/{item_id}")
        def delete_item(model_name: str, item_id: int, _=Depends(self.auth_dependency) if self.auth_dependency else None):
            model = self._get_model(model_name)
            if not model:
                return HTMLResponse("Model not found", status_code=404)

            db = self.session_factory()
            try:
                obj = db.query(model).get(item_id)
                if obj:
                    db.delete(obj)
                    db.commit()
            finally:
                db.close()

            return RedirectResponse(url=f"{prefix}/{model_name}", status_code=302)

    def _get_model(self, model_name: str):
        for m in self.models:
            if m.__name__.lower() == model_name.lower():
                return m
        return None
