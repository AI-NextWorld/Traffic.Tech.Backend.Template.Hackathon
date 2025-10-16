"""Configuración de pruebas.

Ajusta `sys.path` para permitir imports del paquete `app` desde `src/`.
"""

import sys
from pathlib import Path


# Add project src to sys.path so imports like `from app.main import app` work
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
