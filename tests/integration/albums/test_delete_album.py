import json
from os.path import abspath
from unittest import mock
from unittest.mock import PropertyMock

from tests.bootstrap import BaseTestCase, Album


class AlbumDeletionTestCase(BaseTestCase):
    def setUp(self, **kwargs):
        super(AlbumDeletionTestCase, self).setUp()
        self.__album = self._create_album(name="Test Album With Mock 1",
                                          artist="Sargent Peppers and the Lonely QA Engineers Band",
                                          release_date="2018-01-01")

    def tearDown(self):
        super(AlbumDeletionTestCase, self).tearDown()

    def test_delete_plan(self):
        result = self.client.delete(f"/api/albums/{self.__album.id}")

        self.assert200(result)

    def test_delete_plan_with_inexistent_id(self):
        result = self.client.delete(f"/api/albums/999788999")

        self.assert404(result)

    @mock.patch.object(Album, "query", new_callable=PropertyMock)
    def test_delete_plan_with_error(self, mock_obj):
        mock_obj.return_value.filter_by.side_effect = self.raise_exception

        result = self.client.delete(f"/api/albums/{self.__album.id}")

        self.assert500(result)
