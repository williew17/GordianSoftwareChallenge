import requests
import json
from dateutil.parser import isoparse
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=2)

class GordianQuery:
    def __init__(self, key, base_url="https://api.gordiansoftware.com/v2.2/trip"):
        self.LANGUAGE = "en-US"
        self.COUNTRY = "US"
        self.CURRENCY = "USD"
        self.PASSENGER_TYPE = "adult"
        self.GORDIAN_API_KEY = "sandbox_HRx7QsZPcZmSy6j0tyQVX4uYaYWfbPDGo89ftzFZfso08TJjtYOqFgjH"
        self.base_url=base_url

    def createTrip(self):
        passenger = {
            "type": self.PASSENGER_TYPE
        }
        body = {
            "language": self.LANGUAGE,
            "country": self.COUNTRY,
            "currency": self.CURRENCY,
            "passengers": [passenger]
        }
        url = self.base_url
        response = requests.post(url, json=body, auth=(self.GORDIAN_API_KEY, ''))
        response_json = response.json()
        if response.status_code != 201:
            print("Create Trip Failed, error code: {}".format(response.status_code))
            pp.pprint(response_json)
            return False
        trip_id = response_json["trip_id"]
        return trip_id

    def startSearch(self, trip_id, departure_airport, arrival_airport, departure_date, airline):
        journey = {
            "departure_airport": departure_airport,
            "departure_date": departure_date,
            "arrival_date": departure_date,
            "arrival_airport": arrival_airport,
            "marketing_airlines": [airline]
        }
        body = {
            "ticket": {
                "order_by": "duration",
                "search": True,
                "journeys": [journey]
            }
        }
        url = self.base_url + "/{}/search".format(trip_id)
        response = requests.post(url, json=body, auth=(self.GORDIAN_API_KEY, ''))
        response_json = response.json()
        if response.status_code != 201:
            print("Start Search Failed, error code: {}".format(response.status_code))
            pp.pprint(response_json)
            return False
        search_id = response_json["search_id"]
        return search_id
        
    def getSearchResults(self, trip_id, search_id):
        url = self.base_url + "/{}/search/{}/{}".format(trip_id, search_id, "ticket")
        while True:
            response = requests.get(url = url, auth=(self.GORDIAN_API_KEY, ''))
            response_json = response.json()
            if response.status_code != 200:
                print("Get Search Results Failed, error code: {}".format(response.status_code))
                pp.pprint(response_json)
                return False 
            else:
                # get duration price and number of stops
                if response_json["status"] == "failed":
                    print("Search failed.")
                    pp.pprint(response_json)
                    return False
                elif response_json["status"] == "in_progress":
                    print("Search in progress...")
                else:
                    answer = {
                        "durations": [],
                        "number_of_stops": [],
                        "prices": []
                    }
                    # pp.pprint(response_json)
                    tickets = response_json["results"]["products"]["ticket"]
                    for product_id, ticket in tickets.items():
                        segments = ticket["product_details"]["journeys"][0]["segments"]
                        dates = []
                        for segment in segments:
                            dates.append(isoparse(segment["arrival_time"]))
                            dates.append(isoparse(segment["departure_time"]))
                        dates.sort()
                        duration_in_s = (dates[-1]- dates[0]).total_seconds()
                        answer["prices"].append(ticket["price_and_availability"]["group"]["price"]["total"]["amount"]/100)
                        answer["number_of_stops"].append(len(segments)-1)
                        answer["durations"].append(divmod(duration_in_s, 60)[0])
                    answer["min_price"] = round(min(answer["prices"]),2)
                    answer["average_price"] = round(sum(answer["prices"]) / len(answer["prices"]),2)
                    answer["min_duration"] = self.convert_minutes(min(answer["durations"]))
                    answer["average_duration"] = self.convert_minutes(sum(answer["durations"]) / len(answer["durations"]))
                    answer["min_number_of_stops"] = min(answer["number_of_stops"])
                    answer["average_number_of_stops"] = round(sum(answer["number_of_stops"]) / len(answer["number_of_stops"]), 2)
                    return answer
    
    def convert_minutes(self, minutes):
        rounded_minutes = round(minutes)
        hours, remainder = divmod(rounded_minutes, 60)
        return "{} hrs {} minutes".format(hours, remainder)

