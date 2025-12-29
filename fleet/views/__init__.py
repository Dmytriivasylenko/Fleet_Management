# fleet/views/__init__.py
# Пакет, що експортує всі view-функції/класи з підмодулів
from .service import *   # service-history related views
from .vehicle import *   # vehicles related views
from .driver import *    # drivers related views

__all__ = [name for name in globals() if not name.startswith("_")]
