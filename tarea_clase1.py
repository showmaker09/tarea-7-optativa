"""Orquestador de la Actividad 7.

Conecta al clúster existente, crea la base nueva en la primera escritura,
carga el dataset de un solo viaje y audita reprobados con $elemMatch.
"""

from application.services.auditoria_service import (
    consultar_grupos_con_reprobados_exactos,
)
from application.services.carga_masiva_service import ejecutar_carga_masiva_optimizada
from infrastructure.database.cloud_database_manager import CloudDatabaseManager

DATASET_CURSOS = [
    {
        "curso": "Ingeniería de Software Cloud",
        "periodo": "2026-Q3",
        "alumnos": [
            {"nombre": "Ana Gómez", "edad": 22, "estado": "Aprobado"},
            {"nombre": "Carlos Pérez", "edad": 25, "estado": "Reprobado"},
        ],
    },
    {
        "curso": "Arquitectura NoSQL Avanzada",
        "periodo": "2026-Q3",
        "alumnos": [
            {"nombre": "Marta Ruiz", "edad": 22, "estado": "Reprobado"},
            {"nombre": "Luis Castro", "edad": 21, "estado": "Aprobado"},
        ],
    },
    {
        "curso": "Seguridad y Criptografía Perimetral",
        "periodo": "2026-Q3",
        "alumnos": [
            {"nombre": "Sofía Lara", "edad": 24, "estado": "Aprobado"},
            {"nombre": "Diego Marín", "edad": 22, "estado": "Aprobado"},  # Falso positivo potencial
        ],
    },
]


def main() -> None:
    """Ejecuta conexión, carga masiva y consulta con edad objetivo 22."""
    db = CloudDatabaseManager().get_database()
    ejecutar_carga_masiva_optimizada(db, DATASET_CURSOS)

    print("🔍 Consultando grupos con reprobados exactos (edad=22)...")
    resultados = list(consultar_grupos_con_reprobados_exactos(db, 22))

    if not resultados:
        print("⚠️ No se encontraron cursos que cumplan la condición en el mismo subdocumento.")
        return

    for documento in resultados:
        print(f"✅ Curso detectado: {documento.get('curso')} -> {documento.get('alumnos')}")


if __name__ == "__main__":
    main()
