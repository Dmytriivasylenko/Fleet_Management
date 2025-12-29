from __future__ import absolute_import, unicode_literals

# Для забезпечення того, що завдання Celery будуть завантажені при запуску Django
from .celery import app as celery_app

__all__ = ('celery_app',)
