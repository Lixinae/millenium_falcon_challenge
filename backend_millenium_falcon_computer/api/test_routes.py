from unittest import TestCase

from backend_millenium_falcon_computer import create_app


class TestUploadFileApi(TestCase):
    def test_get(self):
        self.fail()

    def test_post_data_ok(self):
        # Todo -> Terminer les test api
        response = self.test_app.post(self.api_route + "upload_and_compute",)

        response_json = response.json
        self.assertTrue("odds_of_success" in response_json)
        self.assertTrue("upload_file_json_answer" in response_json)

    def setUp(self):
        self.test_app = create_app().test_client()
        self.api_route = "/api/"
