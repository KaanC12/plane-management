import os
import json
import requests

API_URL = "http://127.0.0.1:5000"

class Client:
    def __init__(self):
        home = os.path.expanduser("~")
        path = os.path.join(home, ".aircraft", "credentials.json")
        with open(path, "r") as f:
            creds = json.load(f)
        
        encoded_token = creds["token"]
        company_name = creds["company-name"]

        r = requests.post(
            f"{API_URL}/verify-api",
            json={
                "token": encoded_token,
                "company-name": company_name
            }
        )

        if r.status_code != 200:
            raise Exception("login failed. Please check your company name or token.")
    
    def add_station(self, name: str, kw: int, available: bool, lat: float, lng: float):
        r = requests.post(
            f"{API_URL}/add-station",
            json={
                "name": name,
                "kw": kw,
                "isAvailable": available,
                "latitude": lat,
                "longitude": lng,
            }
        )

        if r.status_code != 200:
            raise Exception("Station could not be added.")
        
        
