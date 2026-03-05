from abc import ABC, abstractmethod


class BaseConnector(ABC):
    @abstractmethod
    def init_db(self, *args, **kwargs):
        """
        Initialize the database.

        :param self: Description
        """
        pass

    @abstractmethod
    def get_connection(self):
        """
        Get a connection to the database.

        :param self: Description
        """
        pass

    @abstractmethod
    def close_connection(self):
        """
        Close the connection to the database.

        :param self: Description
        """
