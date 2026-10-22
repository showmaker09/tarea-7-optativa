"""Carga de variables de entorno. No contiene lógica de negocio."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo.errors import ConfigurationError

_RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
load_dotenv(_RAIZ_PROYECTO / ".env")


def get_mongodb_uri() -> str:
    """Devuelve la URI de Atlas. Falla si no existe, sin imprimir su valor."""
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        raise ConfigurationError(
            "La variable MONGODB_URI no está definida. Copia .env.example a .env y completa la URI."
        )
    return uri


def get_db_name() -> str:
    """Devuelve el nombre de la base nueva dentro del clúster existente."""
    nombre = os.getenv("DB_NAME", "").strip()
    if not nombre:
        raise ConfigurationError(
            "La variable DB_NAME no está definida. Copia .env.example a .env y completa el nombre."
        )
    return nombre
