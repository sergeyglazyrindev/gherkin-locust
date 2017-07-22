from gherkin_locust.app import App
from gherkin_locust.settings import Settings
import os
import subprocess


def make_app():

    app = App('test')
    path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'testdb.sqlite3'
        )
    )
    subprocess.call(['cp', os.devnull, path])
    app.use_settings(Settings(
        {'DATABASE': 'sqlite:///' + path}
    ))

    return app
