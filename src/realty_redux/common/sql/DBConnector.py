import inspect
from realty_redux.common import sql


class DBConnector:
    def __new__(cls, engine: str, *args, **kwargs):
        for key, value in inspect.getmembers(sql):
            if engine in key.lower() and key.endswith("Connector"):
                return value(*args, **kwargs)
