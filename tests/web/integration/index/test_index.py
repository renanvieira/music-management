import math
from http import HTTPStatus
from unittest import mock

import lxml.html

from web.resources.error import APIError
from tests.bootstrap import BaseWebTestCase
from web.models import AlbumTable
from web.services import MusicManagementAPIClient


class IndexTestCase(BaseWebTestCase):

    def setUp(self):
        super(IndexTestCase, self).setUp()
        self.data = self._generate_data(15)
        self.total_pages = math.floor(len(self.data) / 10)
        self.total_items = len(self.data)

    def tearDown(self):
        super(IndexTestCase, self).tearDown()

    def test_index(self):
        data_limited = self.data[:10]
        with mock.patch.object(MusicManagementAPIClient, "list_all",
                               return_value=(
                                       AlbumTable(data_limited, self.total_pages, self.total_items), HTTPStatus.OK)):
            result = self.client.get("/")

            self.assert200(result)
            body = lxml.html.fromstring(result.data.decode("utf-8")).body

            # asserting the number of rows inside the table
            trs = body.xpath("//tbody/tr")
            self.assertTrue(len(trs) == len(data_limited))

            # asserting the number of pages
            pagination_buttons = body.xpath("//ul[contains(@class,'pagination')]/li")
            self.assertEqual(self.total_pages,
                             len(pagination_buttons) - 2)  # -2 to exclude the "previous" and "next" buttons

    def test_index_with_api_down(self):
        data_limited = self.data[:10]
        with mock.patch.object(MusicManagementAPIClient, "list_all",
                               side_effect=APIError("Service Is Down")):
            result = self.client.get("/")

            self.assert200(result)
            body = lxml.html.fromstring(result.data.decode("utf-8")).body

            # asserting the number of rows inside the table
            trs = body.xpath("//tbody/tr")
            self.assertEqual(len(trs), 1)

            message = body.xpath("//tbody/tr/td")[0].text
            self.assertEqual("No Albums available to show.", message.strip())


            # asserting the number of pages
            pagination_buttons = body.xpath("//ul[contains(@class,'pagination')]/li")
            self.assertEqual(0,
                             len(pagination_buttons) - 2)  # -2 to exclude the "previous" and "next" buttons

            body = lxml.html.fromstring(result.data.decode("utf-8")).body
            items = body.xpath("//div[contains(@class,'alert')]")
            self.assertEqual(len(items), 1)

            alert_content = body.xpath("//div[contains(@class,'alert')]/text()")[1].strip()
            self.assertEqual("Error trying to load album list.", alert_content)

    def test_empty_index(self):
        data_limited = []
        with mock.patch.object(MusicManagementAPIClient, "list_all",
                               return_value=(
                                       AlbumTable(data_limited, self.total_pages, self.total_items), HTTPStatus.OK)):
            result = self.client.get("/")

            self.assert200(result)
            body = lxml.html.fromstring(result.data.decode("utf-8")).body

            # asserting the number of rows inside the table
            trs = body.xpath("//tbody/tr")
            self.assertEqual(len(trs), 1)

            message = body.xpath("//tbody/tr/td")[0].text
            self.assertEqual("No Albums available to show.", message.strip())

            # asserting the number of pages
            pagination_buttons = body.xpath("//ul[contains(@class,'pagination')]/li")
            self.assertEqual(self.total_pages,
                             len(pagination_buttons) - 2)  # -2 to exclude the "previous" and "next" buttons


