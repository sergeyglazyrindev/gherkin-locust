import os
from unittest import TestCase
import subprocess


class LocustTestCase(TestCase):

    def test(self):
        path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'tests/django/project/db.sqlite3'
            )
        )
        subprocess.call(['cp', os.devnull, path])
        subprocess.Popen(
            ['python tests/django/project/manage.py migrate'],
            shell=True
        )
        subprocess.Popen(
            ['python tests/django/project/manage.py runserver'],
            shell=True
        )
        popen = subprocess.Popen([
            'locust', '-f', 'tests/_locust.py', '--clients=2',
            '--no-web', '--host=http://127.0.0.1:8000'
        ])
        pid = popen.pid
        subprocess.call([
            '''
            sleep 10 && kill {pid}
            '''.format(
                pid=pid
            )
        ], shell=True)
        popen.wait()
        subprocess.call([
            '''
            ps aux |grep manage | grep runserver |
            awk {{'print $2'}} | xargs kill
            '''
        ], shell=True)
        self.assertEquals(popen.returncode, 0)
