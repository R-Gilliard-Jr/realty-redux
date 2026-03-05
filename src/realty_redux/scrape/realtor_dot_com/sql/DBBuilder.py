from sqlalchemy import create_engine, URL, MetaData
from sqlalchemy_utils import database_exists, create_database
from typing import Self


class DBBuilder:
    def __init__(self, metadata: MetaData, **kwargs):
        self.metadata = metadata
        self.gen_engine(**kwargs)

    def gen_engine(self, **kwargs) -> Self:
        """Generate database engine

        Returns:
            Self: Object of class SQLAlchemyUtils
        """

        engine_url = URL.create(**kwargs)
        self._engine = create_engine(engine_url)
        return self

    def create_db(self) -> Self:
        """Create the target database

        Returns:
            Self: Object of class SQLAlchemyUtils
        """

        if not database_exists(self._engine.url):
            create_database(self._engine.url)
            assert database_exists(self._engine.url)

        self.metadata.create_all(self._engine)

        return self


if __name__ == "__main__":
    from realty_redux.scrape.realtor_dot_com.sql.sql_definitions import sql_metadata

    db_path = "C:/Users/regg1/Documents/RealEstateApp/rdc.db"
    DBBuilder(sql_metadata, drivername="sqlite", database=db_path).create_db()
