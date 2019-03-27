from flask import Blueprint

admin = Blueprint(
    "admin", __name__, static_folder="static", template_folder="templates"
)

from app.admin import routes
from app.models import Permission


@admin.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
