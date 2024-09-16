from sqlalchemy import MetaData, create_engine
from settings import Settings

class DatabaseConnection:
    def __init__(self, database=Settings.DB_URI):
        self.database = database
        self.__engine = create_engine(self.database, echo=False)
        self._MetaData = MetaData

    def _create_session(self, query):
        with self.__engine.connect() as conn:
            response = conn.execute(query)
            return response

class query(DatabaseConnection):
    def query(self, query):
        self._create_session(query)
