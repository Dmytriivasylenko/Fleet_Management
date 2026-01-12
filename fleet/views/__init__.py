# fleet/views/__init__.py
# Package that exports all view functions/classes from submodules
from .service import *   # service-history related views
from .vehicle import *   # vehicles related views

__all__ = [name for name in globals() if not name.startswith("_")]
