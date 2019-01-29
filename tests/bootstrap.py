import random
from datetime import datetime
from sqlite3 import DatabaseError

from flask.logging import default_handler
from flask_testing import TestCase

import web
from music_management.app import create_app as api_create_app
from music_management.config import ConfigEnum
from music_management.extensions import db_context
from music_management.models import Album
from web.app import create_app as web_create_app


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        del self.client

        for album in Album.query.all():
            db_context.session.delete(album)

        db_context.session.commit()

    def create_app(self):
        app = api_create_app(ConfigEnum.Testing)
        app.logger.removeHandler(default_handler)

        return app

    def raise_exception(self, *args, **kwargs):
        raise DatabaseError("SELECT 1", {}, "")

    def _create_album(self, name, artist, release_date):
        new_album = Album(name=name, artist=artist, release_date=datetime.strptime(release_date, "%Y-%m-%d"))
        db_context.session.add(new_album)
        db_context.session.commit()

        return new_album


class BaseWebTestCase(TestCase):
    def setUp(self):
        super(BaseWebTestCase, self).setUp()

    def tearDown(self):
        super(BaseWebTestCase, self).tearDown()
        del self.client

    def create_app(self):
        app = web_create_app(web.config.ConfigEnum.Testing)
        app.config["WTF_CSRF_ENABLED"] = False
        app.logger.removeHandler(default_handler)

        return app

    def _generate_data(self, limit=15):
        data = list()
        for i in range(limit):
            new_album = Album(id=i, name=f"Testing Mock Album {i}", artist=f"Mock Artist {i}",
                              release_date=get_random_date(1998))

            data.append(new_album)

        return data


def get_random_date(year):
    # try to get a date
    try:
        return datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y')

    # if the value happens to be in the leap year range, try again
    except ValueError:
        get_random_date(year)
