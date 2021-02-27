import json
from io import BytesIO
from unittest import TestCase

from flask import request, url_for

from backend_millenium_falcon_computer import create_app


class TestUploadFileApi(TestCase):
    def test_get_ok(self):
        with self.test_app:
            self.test_app.get(self.api_route + "upload_and_compute",
                              follow_redirects=True)
            # check that the path changed
            self.assertEqual(url_for('index_bp.index'), request.path)

    def test_post_data_ok(self):
        dict_data = {
            "countdown": 7,
            "bounty_hunters": [
                {
                    "planet": "Hoth",
                    "day": 6
                },
                {
                    "planet": "Hoth",
                    "day": 7
                },
                {
                    "planet": "Hoth",
                    "day": 8
                }
            ]
        }
        input_json = json.dumps(dict_data, indent=4).encode("utf-8")
        data = {
            'file': (BytesIO(input_json), 'empire.json'),  # we use StringIO to simulate file object
        }
        response = self.test_app.post(self.api_route + "upload_and_compute",
                                      data=data,
                                      follow_redirects=True)
        response_json = response.data
        self.assertTrue(b"odds_of_success" in response_json)
        self.assertTrue(b"upload_file_json_answer" in response_json)
        self.assertTrue(b"trajectory" in response_json)
        self.assertTrue(b"refueled_on" in response_json)

    def test_post_data_nok(self):
        dict_data = {
            "countdown": 7,
            "bounty_hunters": [
                {
                    "planet": "Hoth",
                    "day": 6
                },
                {
                    "planet": "Hoth",
                    "day": 7
                },
                {
                    "planet": "Hoth",
                    "day": 8
                }
            ]
        }
        input_json = json.dumps(dict_data, indent=4).encode("utf-8")
        data = {
            'file': (BytesIO(input_json), 'empire.txt'),  # we use StringIO to simulate file object
        }
        response = self.test_app.post(self.api_route + "upload_and_compute",
                                      data=data,
                                      follow_redirects=True)
        response_json = response.data
        self.assertTrue(b"null\n" in response_json)

    def setUp(self):
        self.test_app = create_app().test_client()
        self.api_route = "/api/"
