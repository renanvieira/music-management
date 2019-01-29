import json
import os
from http import HTTPStatus
from unittest.mock import patch, Mock

from tests.bootstrap import BaseWebTestCase
from web.resources.error import APIError, APIValidationError
from web.services import MusicManagementAPIClient


class ApiServiceTestCase(BaseWebTestCase):

    def setUp(self):
        self.response_files = dict()
        responses_folder_path = f"{os.path.dirname(os.path.realpath(__file__))}/mock_responses"
        for dirname, dirnames, filenames in os.walk(responses_folder_path):
            for file in filenames:
                self.response_files[file.split(".")[0]] = json.loads(
                    open(f"{responses_folder_path}/{file}", 'r').read())

    @patch('requests.get')
    def test_list_all_albums(self, get_mock):
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = self.response_files["list_all_response"]
        get_mock.return_value = mocked_response

        albums, status_code = MusicManagementAPIClient.list_all(1)

        self.assertIsNotNone(albums)
        self.assertEqual(len(albums.items), 10)
        self.assertEqual(albums.total_items, 12)
        self.assertEqual(albums.total_pages, 2)
        self.assertEqual(status_code, HTTPStatus.OK)

    @patch('requests.get')
    def test_list_all_albums_with_error(self, get_mock):
        with self.assertRaises(APIError):
            get_mock.side_effect = ConnectionError("Host is down")

            albums, status_code = MusicManagementAPIClient.list_all(1)

    @patch('requests.get')
    def test_get_album_by_id(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = self.response_files["get_album_by_id"]
        post_mock.return_value = mocked_response

        albums, status_code = MusicManagementAPIClient.get_album_by_id(5)

        self.assertEqual(status_code, HTTPStatus.OK)

    @patch('requests.get')
    def test_get_album_by_id_404(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = HTTPStatus.NOT_FOUND
        mocked_response.json.return_value = dict(error={"message": "Resource Not Found."})
        post_mock.return_value = mocked_response

        albums, status_code = MusicManagementAPIClient.get_album_by_id(5)

        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)

    @patch('requests.get')
    def test_get_album_by_id_with_error(self, get_mock):
        with self.assertRaises(APIError):
            get_mock.side_effect = ConnectionError("Host is down")

            albums, status_code = MusicManagementAPIClient.get_album_by_id(1)

    @patch('requests.post')
    def test_add_album(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = self.response_files["get_album_by_id"]
        post_mock.return_value = mocked_response

        data = {
            "artist": "Oasis",
            "name": "(What's the Story) Morning Glory?",
            "release_date": "1995-10-06"

        }

        albums, status_code = MusicManagementAPIClient.add_album(data)

        self.assertEqual(status_code, HTTPStatus.OK)
        self.assertIsNotNone(albums["created_at"])
        self.assertIsNone(albums["updated_at"])

    @patch('requests.post')
    def test_add_album_with_validation_error(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = HTTPStatus.BAD_REQUEST
        mocked_response.json.return_value = dict(
            error={"validation_errors": [dict(field="artist", message="Missing data for required field.")]})
        post_mock.return_value = mocked_response

        data = {
            "name": "(What's the Story) Morning Glory?",
            "release_date": "1995-10-06"

        }

        with self.assertRaises(APIValidationError):
            albums, status_code = MusicManagementAPIClient.add_album(data)

    @patch('requests.post')
    def test_add_album_with_connection_error(self, post_mock):
        post_mock.side_effect = ConnectionError("Host is Down")

        data = {
            "name": "(What's the Story) Morning Glory?",
            "release_date": "1995-10-06"

        }

        with self.assertRaises(APIError):
            albums, status_code = MusicManagementAPIClient.add_album(data)

    @patch('requests.post')
    def test_update_album(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = self.response_files["updated_album"]
        post_mock.return_value = mocked_response

        data = {
            "artist": "Oasis",
            "name": "Be Here Now",
            "release_date": "1995-10-06"
        }

        albums, status_code = MusicManagementAPIClient.update_album(5, data)

        self.assertEqual(status_code, HTTPStatus.OK)
        self.assertIsNotNone(albums["created_at"])
        self.assertIsNotNone(albums["updated_at"])

    @patch('requests.post')
    def test_update_album_404(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 404
        mocked_response.json.return_value = dict(error={"message": "Resource Not Found."})
        post_mock.return_value = mocked_response

        data = {
            "artist": "Oasis",
            "name": "Be Here Now",
            "release_date": "1995-10-06"
        }

        albums, status_code = MusicManagementAPIClient.update_album(5, data)

        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)

    @patch('requests.post')
    def test_update_album_with_validation_error(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 400
        mocked_response.json.return_value = dict(
            error={"validation_errors": [dict(field="artist", message="Missing data for required field.")]})
        post_mock.return_value = mocked_response

        data = {
            "name": "Be Here Now",
            "release_date": "1995-10-06"
        }

        with self.assertRaises(APIValidationError):
            albums, status_code = MusicManagementAPIClient.update_album(5, data)

    @patch('requests.post')
    def test_update_album_with_connection_error(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 400
        mocked_response.side_effect = ConnectionError("Host Is Down")
        post_mock.return_value = mocked_response

        data = {
            "name": "Be Here Now",
            "release_date": "1995-10-06"
        }

        with self.assertRaises(APIError):
            albums, status_code = MusicManagementAPIClient.update_album(5, data)

    @patch('requests.delete')
    def test_delete_album(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = self.response_files["deleted_album"]
        post_mock.return_value = mocked_response

        albums, status_code = MusicManagementAPIClient.delete_album(5)

        self.assertEqual(status_code, HTTPStatus.OK)
        self.assertIsNotNone(albums["created_at"])
        self.assertIsNotNone(albums["updated_at"])
        self.assertIsNotNone(albums["deleted_at"])

    @patch('requests.delete')
    def test_delete_album_404(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 404
        mocked_response.json.return_value = dict(error={"message": "Resource Not Found."})
        post_mock.return_value = mocked_response

        data = {
            "artist": "Oasis",
            "name": "Be Here Now",
            "release_date": "1995-10-06"
        }

        albums, status_code = MusicManagementAPIClient.delete_album(5)

        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)

    @patch('requests.delete')
    def test_delete_album_with_connection_error(self, post_mock):
        mocked_response = Mock()
        mocked_response.status_code = 400
        mocked_response.side_effect = ConnectionError("Host Is Down")
        post_mock.return_value = mocked_response

        data = {
            "name": "Be Here Now",
            "release_date": "1995-10-06"
        }

        with self.assertRaises(APIError):
            albums, status_code = MusicManagementAPIClient.delete_album(5)
