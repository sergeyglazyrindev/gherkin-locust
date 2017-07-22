from unittest import TestCase
from .helpers import make_app
from gherkin_locust.models import User


class AppTestCase(TestCase):

    def test(self):
        app = make_app()
        self.assertTrue(bool(app))

    def test_db_session(self):
        app = make_app()
        session = app.db_session()
        user = User(id=1, email='dasdas')
        session.add(user)
        session.commit()
        user = session.query(User).filter_by(
            email='dasdas'
        ).one()
