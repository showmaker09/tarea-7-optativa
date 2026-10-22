"""Carga masiva de cursos en un solo viaje de red."""

from typing import Any

from pymongo.database import Database
from pymongo.errors import BulkWriteError
from pymongo.results import InsertManyResult


def ejecutar_carga_masiva_optimizada(
    db: Database, datos: list[dict[str, Any]]
) -> InsertManyResult:
    """Inserta el lote completo con `insert_many(ordered=False)`.

    Un solo `insert_many` sustituye varios `insertOne` y evita saturar
    la red por el RTT de cada documento. `ordered=False` deja que el
    servidor continúe con el resto del lote si un documento falla.
    """
    coleccion = db["cursos_auditoria"]
    try:
        resultado = coleccion.insert_many(datos, ordered=False)
        print(
            f"✅ Carga masiva completada. Documentos insertados: {len(resultado.inserted_ids)}"
        )
        return resultado
    except BulkWriteError as error:
        insertados = (error.details or {}).get("nInserted", 0)
        print(
            f"❌ Error durante la carga masiva: {error}. "
            f"Documentos insertados antes del fallo: {insertados}"
        )
        raise
    except Exception as error:
        print(f"❌ Error durante la carga masiva: {error}")
        raise
