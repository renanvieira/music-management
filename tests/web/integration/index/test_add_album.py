import math
from http import HTTPStatus
from unittest import mock

import lxml.html
from flask import url_for

from web.resources.error import APIError
from tests.bootstrap import BaseWebTestCase
from web.services import MusicManagementAPIClient


class AddAlbumTestCase(BaseWebTestCase):

    def setUp(self):
        super(AddAlbumTestCase, self).setUp()
        self.data = self._generate_data(15)
        self.total_pages = math.floor(len(self.data) / 10)
        self.total_items = len(self.data)

    def tearDown(self):
        super(AddAlbumTestCase, self).tearDown()

    def test_get_add_page(self):
        result = self.client.get("/add")

        self.assert200(result)

    def test_post_add_page(self):
        post_data = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")
        mock_return = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")

        with mock.patch.object(MusicManagementAPIClient, "add_album", lambda p: (mock_return, HTTPStatus.OK)):
            result = self.client.post(url_for("album.add"), data=post_data)
            self.assert_redirects(result, "/")

            with self.client.session_transaction() as session:
                flash_message = session["_flashes"][0]
                self.assertEqual(len(session["_flashes"]), 1)
                self.assertEqual(flash_message[1], "Album added successfully.")
                self.assertEqual(flash_message[0], "success")

    def test_post_add_page_with_validation_error(self):
        mock_data = dict(name="The Mock", release_date="2019-01-20")

        with mock.patch.object(MusicManagementAPIClient, "add_album", lambda p: (mock_data, HTTPStatus.BAD_REQUEST)):
            result = self.client.post(url_for("album.add"), data=mock_data)
            self.assert200(result)

            body = lxml.html.fromstring(result.data.decode("utf-8")).body
            items = body.xpath("//div[contains(@class,'alert')]/ul/li")
            self.assertEqual(len(items), 1)

            field_name = body.xpath("//div[contains(@class,'alert')]/ul/li/strong")[0].text
            self.assertTrue("artist name:" in field_name.lower())

            message = body.xpath("//div[contains(@class,'alert')]/ul/li/text()")[0]
            self.assertTrue("field is required" in message.lower())

    def test_post_add_page_with_api_down(self):
        post_data = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")
        mock_return = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")

        with mock.patch.object(MusicManagementAPIClient, "add_album", side_effect=APIError("Service is Down")):
            result = self.client.post(url_for("album.add"), data=post_data)
            self.assert200(result)

            body = lxml.html.fromstring(result.data.decode("utf-8")).body
            items = body.xpath("//div[contains(@class,'alert')]")
            self.assertEqual(len(items), 1)

            alert_content = body.xpath("//div[contains(@class,'alert')]/text()")[1].strip()
            self.assertEqual("Error trying to adding a new album.", alert_content)

    def test_post_add_page_with_api_return_not_200(self):
        post_data = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")
        mock_return = dict(artist="Testing Mock", name="The Mock", release_date="2019-01-20")

        with mock.patch.object(MusicManagementAPIClient, "add_album", lambda p: (None, HTTPStatus.INTERNAL_SERVER_ERROR)):
            result = self.client.post(url_for("album.add"), data=post_data)
            self.assert200(result)

            body = lxml.html.fromstring(result.data.decode("utf-8")).body
            items = body.xpath("//div[contains(@class,'alert')]")
            self.assertEqual(len(items), 1)

            alert_content = body.xpath("//div[contains(@class,'alert')]/text()")[1].strip()
            self.assertEqual("Error while trying to talk with API: API returned HTTP 500.", alert_content)
