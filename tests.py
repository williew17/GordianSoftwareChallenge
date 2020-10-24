
import unittest
from unittest.mock import Mock, patch
# from app import app
from app.gordian import GordianQuery
from config import Config
# from app.form import TripSearchForm
# from flask import render_template
API_KEY = Config.GORDIAN_API_KEY
class TestGordian(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        self.gord = GordianQuery(API_KEY)

    def tearDown(self):
        pass 
    
    @patch('app.gordian.requests.post')
    def test_createTrip_success(self, mock_get):
        mock_get.return_value.status_code = 201
        mock_get.return_value.json.return_value = {"trip_id": "dummy_id"}
        result = self.gord.createTrip()
        # assert the status code of the response
        self.assertEqual(result, "dummy_id") 

    @patch('app.gordian.requests.post')
    def test_createTrip_failed(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {"trip_id": "dummy_id"}
        result = self.gord.createTrip()
        self.assertEqual(result, False)

    @patch('app.gordian.requests.post')
    def test_startSearch_success(self, mock_get):
        mock_get.return_value.status_code = 201
        mock_get.return_value.json.return_value = {"search_id": "dummy_id"}
        result = self.gord.startSearch("dummy_trip_id", "SFO", "LAX", "2020-10-30", "WN")
        self.assertEqual(result, "dummy_id")
    
    @patch('app.gordian.requests.post')
    def test_startSearch_failed(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {"trip_id": "dummy_id"}
        result = self.gord.startSearch("dummy_trip_id", "SFO", "LAX", "2020-10-30", "WN")
        self.assertEqual(result, False)

    @patch('app.gordian.requests.get')
    def test_getSearchResults_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "status": "success",
            "results": {
                "products": {
                    "ticket": {
                        "dummy_product_id0" : {
                            "price_and_availability": {"group": {"price": {"total": {"amount" : 100 } } } },
                            "product_details": {
                                "journeys": [
                                    {
                                        "segments": [
                                            {
                                                "arrival_time": '2020-10-24T11:00:00-07:00',
                                                "departure_time": '2020-10-24T10:00:00-07:00'
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        "dummy_product_id1" : {
                            "price_and_availability": {"group": {"price": {"total": {"amount" : 200 } } } },
                            "product_details": {
                                "journeys": [
                                    {
                                        "segments": [
                                            {
                                                "arrival_time": '2020-10-24T11:00:00-07:00',
                                                "departure_time": '2020-10-24T09:00:00-07:00'
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        "dummy_product_id2" : {
                            "price_and_availability": {"group": {"price": {"total": {"amount" : 300 } } } },
                            "product_details": {
                                "journeys": [
                                    {
                                        "segments": [
                                            {
                                                "arrival_time": '2020-10-24T11:00:00-07:00',
                                                "departure_time": '2020-10-24T10:00:00-07:00'
                                            },
                                            {
                                                "arrival_time": '2020-10-24T10:00:00-07:00',
                                                "departure_time": '2020-10-24T08:00:00-07:00'
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
        result = self.gord.getSearchResults("dummy_trip_id", "dummy_search_id")
        expected = {
            "durations": [60.0, 120.0, 180.0],
            "number_of_stops": [0, 0, 1],
            "prices": [1.0, 2.0, 3.0],
            "min_price": 1.00,
            "average_price": 2.00,
            "min_duration": "1 hrs 0 minutes",
            "average_duration": "2 hrs 0 minutes",
            "min_number_of_stops": 0,
            "average_number_of_stops": 0.33
        }
        self.assertEqual(result, expected)

    @patch('app.gordian.requests.get')
    def test_getSearchResults_failed(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = { "status": "failed" }
        result = self.gord.getSearchResults("dummy_trip_id", "dummy_search_id")
        self.assertEqual(result, False)