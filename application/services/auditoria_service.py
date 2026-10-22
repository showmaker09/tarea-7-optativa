"""Auditoría de reprobados sobre el mismo subdocumento del arreglo."""

from pymongo.cursor import Cursor
from pymongo.database import Database


def consultar_grupos_con_reprobados_exactos(db: Database, edad_objetivo: int) -> Cursor:
    """Busca cursos con un alumno de la edad indicada y estado Reprobado.

    `$elemMatch` evalúa `edad` y `estado` en el mismo elemento de `alumnos`.
    Así se descartan falsos positivos en los que un alumno cumple la edad
    y otro, distinto, está reprobado.

    La proyección omite `_id` y, con el operador posicional `$`, devuelve
    solo el subdocumento que hizo match.
    """
    coleccion = db["cursos_auditoria"]

    query = {
        "alumnos": {
            "$elemMatch": {
                "edad": edad_objetivo,
                "estado": "Reprobado",
            }
        }
    }

    projection = {
        "_id": 0,
        "curso": 1,
        "alumnos.$": 1,
    }

    return coleccion.find(query, projection)
