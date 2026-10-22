"""Conexión única (Singleton) hacia MongoDB Atlas."""

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConfigurationError, ConnectionFailure

from config.settings import get_db_name, get_mongodb_uri


class CloudDatabaseManager:
    """Administra un solo cliente y una sola base de datos por proceso.

    `_client_instance` y `_database_instance` evitan abrir conexiones
    duplicadas contra el mismo clúster.
    """

    _instance = None
    _client_instance = None
    _database_instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if CloudDatabaseManager._client_instance is None:
            self._conectar()

    def _conectar(self) -> None:
        """Valida la configuración, abre el cliente y confirma el clúster con ping."""
        try:
            uri = get_mongodb_uri()
            nombre_db = get_db_name()
        except ConfigurationError as error:
            print(f"❌ Configuración inválida: {error}")
            raise

        try:
            cliente = MongoClient(
                uri,
                serverSelectionTimeoutMS=5000,
                tls=True,
            )
            cliente.admin.command("ping")
        except ConnectionFailure as error:
            print(f"❌ No se pudo alcanzar MongoDB Atlas: {error}")
            raise
        except ConfigurationError as error:
            print(f"❌ La URI de MongoDB no es válida: {error}")
            raise

        CloudDatabaseManager._client_instance = cliente
        # Atlas crea la base en la primera escritura; aquí solo se selecciona.
        CloudDatabaseManager._database_instance = cliente[nombre_db]
        print(f"✅ Conexión establecida. Base de datos seleccionada: {nombre_db}")

    def get_database(self) -> Database:
        """Devuelve la instancia única de la base de datos."""
        if CloudDatabaseManager._database_instance is None:
            self._conectar()
        return CloudDatabaseManager._database_instance
