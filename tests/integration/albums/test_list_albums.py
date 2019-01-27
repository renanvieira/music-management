import random
from datetime import datetime
from unittest import mock
from unittest.mock import PropertyMock

from music_management.extensions import db_context
from tests.bootstrap import BaseTestCase, Album


class AlbumListTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(AlbumListTestCase, self).setUp()
        self.__albums = list()
        for i in range(1, 9):
            self.__albums.append(self._create_album(name=f"Test Album With Mock {i}",
                                                    artist="Sargent Peppers and the Lonely QA Engineers Band",
                                                    release_date=f"2018-01-{i}"))

        album = random.choice(self.__albums)
        album.deleted_at = datetime.utcnow()
        db_context.session.add(album)
        db_context.session.commit()


    def tearDown(self):
        super(AlbumListTestCase, self).tearDown()

    def test_list_albumss(self):
        result = self.client.get(f"/api/albums")

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertEqual(result.json["total"], 7)

    def test_list_albums_including_deleted(self):
        result = self.client.get(f"/api/albums?deleted=true")

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertEqual(result.json["total"], 8)


    @mock.patch.object(Album, "query", new_callable=PropertyMock)
    def test_list_albums_with_error(self, mock_obj):
        mock_obj.return_value.filter.side_effect = self.raise_exception

        result = self.client.get(f"/api/albums")

        self.assert500(result)
