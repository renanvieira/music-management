from unittest import mock
from unittest.mock import PropertyMock

from flask import json

from tests.bootstrap import BaseTestCase, Album


class AlbumCreationTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(AlbumCreationTestCase, self).setUp()
        self.first_album = self._create_album(name="Test Album With Mock 1",
                                         artist="Sargent Peppers and the Lonely QA Engineers Band",
                                         release_date="2018-01-01")


    def tearDown(self):
        super(AlbumCreationTestCase, self).tearDown()

    def test_create_album(self):
        json_str = """{
            "artist": "Reel Big Fish",
            "name": "Life Sucks...Let's Dance",
            "release_date": "10/12/2018"
        }"""

        result = self.client.post("/api/albums", json=json.loads(json_str))

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertTrue(isinstance(result.json["id"], int))

    @mock.patch.object(Album, "query", new_callable=PropertyMock)
    def test_create_album_with_error(self, mock_obj):
        mock_obj.return_value.filter_by.side_effect = self.raise_exception

        new_data = {
            "name": "Test Album With Mock 1",
            "artist": "Sargent Peppers and the Lonely QA Engineers Band"
        }

        result = self.client.post(f"/api/albums", json=new_data)

        self.assert500(result)

    def test_create_album_without_name(self):
        data = {
            "artist": "Sargent Peppers and the Lonely QA Engineers Band"
        }

        result = self.client.post("/api/albums", json=data)

        self.assert400(result)

    def test_create_albums_with_same_name_and_artist(self):

        new_data = {
            "name": "Test Album With Mock 1",
            "artist": "Sargent Peppers and the Lonely QA Engineers Band",
            "release_date": "2018-01-01"
        }

        result2 = self.client.post("/api/albums", json=new_data)

        self.assert400(result2)
