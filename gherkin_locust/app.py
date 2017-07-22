from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db import Base


class App:

    def __init__(self, name):
        """Initializes application

        :param name: Name of your application
        :type name: str
        :returns: nothing
        :rtype: None
        """
        self.name = name

    def use_settings(self, settings):
        """App will use settings passed to this func

        :param settings: Please pass Settings object here
        :type settings: :class:`gherkin_locust.settings.Settings`
        :returns: nothing
        :rtype: None

        """
        self.settings = settings

    def db_session(self):
        if hasattr(self, '_db_session'):
            return self._db_session
        engine = create_engine(self.settings.DATABASE)
        Base.metadata.create_all(engine)
        self._db_session = sessionmaker(bind=engine)()
        return self._db_session
