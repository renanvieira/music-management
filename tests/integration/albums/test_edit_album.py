from unittest import mock
from unittest import mock
from unittest.mock import PropertyMock

from tests.bootstrap import BaseTestCase, Album


class AlbumEditTestCase(BaseTestCase):

    def setUp(self, **kwargs):
        super(AlbumEditTestCase, self).setUp()
        self.__album = self._create_album(name="Test Album With Mock 1",
                                          artist="Sargent Peppers and the Lonely QA Engineers Band",
                                          release_date="2018-01-01")

    def tearDown(self):
        super(AlbumEditTestCase, self).tearDown()

    def test_edit_album(self):
        new_data = {
            "name": "Summer Album 1"
        }

        result = self.client.post(f"/api/albums/{self.__album.id}", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertTrue(isinstance(result.json["id"], int))
        self.assertEqual(result.json["name"], new_data["name"])

    def test_edit_album_changing_name_and_artist(self):
        new_data = {
            "name": "Summer Album 1",
            "artist": "The Testing Band"
        }

        result = self.client.post(f"/api/albums/{self.__album.id}", json=new_data)

        self.assert200(result)
        self.assertIsNotNone(result.json)
        self.assertIn("id", result.json)
        self.assertTrue(isinstance(result.json["id"], int))
        self.assertEqual(result.json["name"], new_data["name"])

    def test_edit_album_with_long_name(self):
        new_data = {
            "name": "Boca-newlywed-shutout-playbill-surprise-onetime-goddess-tincture-bacon-couplet-Glisten-haul-lazar-undies-campfire-reproof-sensor-upraise-sealskin-pulp"
        }

        result = self.client.post(f"/api/albums/{self.__album.id}", json=new_data)

        self.assert400(result)

    def test_edit_album_with_invalid_id(self):
        new_data = {
            "name": "Testing Edit Album 1"
        }
        result = self.client.post(f"/api/albums/{99999}", json=new_data)

        self.assert404(result)

    def test_edit_album_with_same_name(self):
        new_data = {
            "name": self.__album.name
        }

        result = self.client.post(f"/api/albums/{self.__album.id}", json=new_data)

        self.assert400(result)

    @mock.patch.object(Album, "query", new_callable=PropertyMock)
    def test_edit_album_with_error(self, mock_obj):
        mock_obj.return_value.filter.side_effect = self.raise_exception

        new_data = {
            "name": "Testing Edit Album 3"
        }

        result = self.client.post(f"/api/albums/{self.__album.id}", json=new_data)

        self.assert500(result)
