from http import HTTPStatus
from unittest import mock
from unittest.mock import PropertyMock

from music_management.models import Album
from tests.bootstrap import BaseTestCase


class GetAlbumTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(GetAlbumTestCase, self).setUp()

        self.__album = self._create_album(name="Test Album With Mock 1",
                                          artist="Sargent Peppers and the Lonely QA Engineers Band",
                                          release_date="2018-01-01")

    def tearDown(self):
        super(GetAlbumTestCase, self).tearDown()

    def test_get_album(self):
        result = self.client.get(f"/api/albums/{self.__album.id}")

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertTrue("id" in result.json)
        self.assertIsNotNone(result.json["id"])
        self.assertTrue(isinstance(result.json["id"], int))
        self.assertIn("created_at", result.json)
        self.assertIn("updated_at", result.json)
        self.assertIn("deleted_at", result.json)

    def test_get_album_with_invalid_id(self):
        result = self.client.get(f"/api/albums/{99999}")

        assert result.status_code == HTTPStatus.NOT_FOUND

    @mock.patch.object(Album, "query", new_callable=PropertyMock)
    def test_get_album_with_error(self, mock_obj):
        mock_obj.return_value.filter.side_effect = self.raise_exception

        result = self.client.get(f"/api/albums/{self.__album.id}")

        self.assert500(result)
