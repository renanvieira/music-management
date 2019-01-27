from datetime import datetime
from sqlite3 import DatabaseError

from flask.testing import FlaskClient
from flask_testing import TestCase

from music_management.app import create_app
from music_management.config import ConfigEnum
from music_management.extensions import db_context
from music_management.models import Album


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
        app = create_app(ConfigEnum.Testing)

        return app

    def raise_exception(self, *args, **kwargs):
        raise DatabaseError("SELECT 1", {}, "")

    def _create_album(self, name, artist, release_date):

        new_album = Album(name=name, artist=artist, release_date=datetime.strptime(release_date, "%Y-%m-%d"))
        db_context.session.add(new_album)
        db_context.session.commit()

        return new_album
