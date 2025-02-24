# __init__.py (inside your_project)
from .celery import app as celery_app

__all__ = ['celery_app']