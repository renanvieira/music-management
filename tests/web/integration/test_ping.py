from tests.bootstrap import BaseTestCase, BaseWebTestCase


class PingTestCase(BaseWebTestCase):
    def setUp(self, **kwargs):
        super(PingTestCase, self).setUp()

    def tearDown(self):
        super(PingTestCase, self).tearDown()

    def test_ping(self):
        result = self.client.get("/ping")
        self.assert200(result)
        self.assertEqual(result.data.decode("utf-8"), "Web Pong!")
