import copy
import math
import random
from http import HTTPStatus
from unittest import mock

import lxml.html
from flask import url_for

from tests.bootstrap import BaseWebTestCase
from web.resources.error import APIError
from web.services import MusicManagementAPIClient


class EditAlbumTestCase(BaseWebTestCase):

    def setUp(self):
        super(EditAlbumTestCase, self).setUp()
        self.data = self._generate_data(15)
        self.total_pages = math.floor(len(self.data) / 10)
        self.total_items = len(self.data)

    def tearDown(self):
        super(EditAlbumTestCase, self).tearDown()

    def test_get_edit_page(self):
        mock_return = random.choice(self.data)
        with mock.patch.object(MusicManagementAPIClient, "get_album_by_id", lambda p: (mock_return, HTTPStatus.OK)):
            result = self.client.get(url_for("album.edit", id=mock_return.id))

            self.assert200(result)
            body = lxml.html.fromstring(result.data.decode("utf-8")).body

            csrf_input = body.xpath("//form/input[@name='csrf_token']")
            self.assertEqual(len(csrf_input), 1)

            inputs = body.xpath("//form/div/div/input")
            self.assertEqual(len(inputs), 3)

            form_artist = body.xpath("//form/div/div/input[@name='artist']")[0].value
            form_album_name = body.xpath("//form/div/div/input[@name='name']")[0].value
            form_release_date = body.xpath("//form/div/div/input[@name='release_date']")[0].value

            self.assertEqual(mock_return.artist, form_artist)
            self.assertEqual(mock_return.name, form_album_name)
            self.assertEqual(mock_return.release_date.strftime("%Y-%m-%d %H:%M:%S"), form_release_date)

    def test_post_edit_page(self):
        mock_return = random.choice(self.data)
        post_data = dict(name="Auei", artist=mock_return.artist,
                         release_date=mock_return.release_date.strftime("%Y-%m-%d"))

        mock_edited = copy.deepcopy(mock_return)
        mock_edited.name = post_data["name"]

        with mock.patch.object(MusicManagementAPIClient, "get_album_by_id", lambda p: (mock_return, HTTPStatus.OK)):
            with mock.patch.object(MusicManagementAPIClient, "update_album",
                                   lambda p, data: (mock_edited, HTTPStatus.OK)):
                result = self.client.post(url_for("album.edit", id=mock_return.id), data=post_data)
                self.assert_redirects(result, "/")

                with self.client.session_transaction() as session:
                    flash_message = session["_flashes"][0]
                    self.assertEqual(len(session["_flashes"]), 1)
                    self.assertEqual(flash_message[1], "Album updated successfully.")
                    self.assertEqual(flash_message[0], "success")

    def test_post_edit_page_with_validation_error(self):
        mock_data = dict(name="The Mock", release_date="2019-01-20")
        mock_return = random.choice(self.data)
        post_data = dict(name="Auei", artist=mock_return.artist)

        with mock.patch.object(MusicManagementAPIClient, "add_album", lambda p: (mock_data, HTTPStatus.OK)):
            result = self.client.post(url_for("album.edit", id=mock_return.id), data=post_data)
            self.assert200(result)

            body = lxml.html.fromstring(result.data.decode("utf-8")).body
            items = body.xpath("//div[contains(@class,'alert')]/ul/li")
            self.assertEqual(len(items), 1)

            field_name = body.xpath("//div[contains(@class,'alert')]/ul/li/strong")[0].text
            self.assertTrue("release date:" in field_name.lower())

            message = body.xpath("//div[contains(@class,'alert')]/ul/li/text()")[0]
            self.assertTrue("field is required" in message.lower())

    def test_get_edit_page_with_api_down(self):
        with mock.patch.object(MusicManagementAPIClient, "get_album_by_id", side_effect=APIError()):
            result = self.client.get(url_for("album.edit", id=1))
            self.assert200(result)

            body = lxml.html.fromstring(result.data.decode("utf-8")).body
            items = body.xpath("//div[contains(@class,'alert')]")
            self.assertEqual(len(items), 1)

            alert_content = body.xpath("//div[contains(@class,'alert')]/text()")[1].strip()
            self.assertEqual("Error trying to load album details.", alert_content)

    def test_post_edit_page_with_api_down(self):
        post_data = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")

        with mock.patch.object(MusicManagementAPIClient, "update_album", side_effect=APIError()):
            result = self.client.post(url_for("album.edit", id=1), data=post_data)
            self.assert200(result)

            body = lxml.html.fromstring(result.data.decode("utf-8")).body
            items = body.xpath("//div[contains(@class,'alert')]")
            self.assertEqual(len(items), 1)

            alert_content = body.xpath("//div[contains(@class,'alert')]/text()")[1].strip()
            self.assertEqual("Something went wrong while trying to update the requested album.", alert_content)

    def test_get_edit_page_with_api_return_not_200(self):
        post_data = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")
        mock_return = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")

        with mock.patch.object(MusicManagementAPIClient, "get_album_by_id",
                               lambda p: (None, HTTPStatus.INTERNAL_SERVER_ERROR)):
            result = self.client.get(url_for("album.edit", id=1))
            self.assertRedirects(result, url_for("album.index"))

            with self.client.session_transaction() as session:
                flash_message = session["_flashes"][0]
                self.assertEqual(len(session["_flashes"]), 1)
                self.assertEqual(flash_message[1], "Something went wrong while trying to load the requested album.")
                self.assertEqual(flash_message[0], "danger")

    def test_post_edit_page_with_api_return_not_200(self):
        post_data = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")
        mock_return = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")

        with mock.patch.object(MusicManagementAPIClient, "update_album",
                               lambda id, p: (None, HTTPStatus.INTERNAL_SERVER_ERROR)):
            result = self.client.post(url_for("album.edit", id=1), data=post_data)
            self.assertRedirects(result, url_for("album.index"))

            with self.client.session_transaction() as session:
                flash_message = session["_flashes"][0]
                self.assertEqual(len(session["_flashes"]), 1)
                self.assertEqual(flash_message[1], "Something went wrong while trying to update the requested album.")
                self.assertEqual(flash_message[0], "danger")

