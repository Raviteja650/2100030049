from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import requests

# Constants
WINDOW_SIZE = 10
window = []

# URLs for the test server endpoints
AUTH_URL = 'http://20.244.56.144/test/auth'
TEST_SERVER_URLS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand',
}

AUTH_PAYLOAD = {
    "companyName": "kL University",
    "clientID": "2999339c-f3c6-40dd-bd99-a3e53dae15ad",
    "clientSecret": "qsYODfEAqKiSdYbP",
    "ownerName": "B.Ravi Teja Reddy",
    "ownerEmail": "2100030049cseh1@gmail.com",
    "rollNo": "2100030049"
}

REQUEST_TIMEOUT = 5 



def fetch_token():
    try:
        response = requests.post(AUTH_URL, json=AUTH_PAYLOAD, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        access_token = data.get('access_token')
        if access_token:
            print("Access token successfully retrieved.")
        else:
            print("Failed to retrieve access token: No access_token in response.")
        return access_token
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching token: {http_err}")
    except requests.RequestException as req_err:
        print(f"Request exception occurred while fetching token: {req_err}")
    return None

def fetch_numbers(numberid):
    url = TEST_SERVER_URLS.get(numberid)
    if not url:
        print(f"Invalid number ID: {numberid}")
        return None

    token = fetch_token()
    if not token:
        print("Failed to fetch token.")
        return None

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        numbers = data.get('numbers', [])
        return numbers
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching numbers: {http_err}")
    except requests.RequestException as req_err:
        print(f"Request exception occurred while fetching numbers: {req_err}")
    return None

class CalculatorAPIView(APIView):

    def get(self, request, numberid, format=None):
        global window

        if numberid not in TEST_SERVER_URLS:
            return Response({"error": "Invalid number ID"}, status=status.HTTP_400_BAD_REQUEST)

        new_numbers = fetch_numbers(numberid)
        if new_numbers is None:
            return Response({"error": "Failed to fetch numbers from the test server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        window_prev_state = list(window)

        for number in new_numbers:
            if number not in window:
                if len(window) >= WINDOW_SIZE:
                    window.pop(0)
                window.append(number)

        avg = sum(window) / len(window) if window else 0

        
        numbers_str = ', '.join(map(str, new_numbers))
        window_prev_state_str = ', '.join(map(str, window_prev_state))
        window_curr_state_str = ', '.join(map(str, window))

        response_data = {
            "numbers": f"[{numbers_str}]",
            "windowPrevState": f"[{window_prev_state_str}]",
            "windowCurrState": f"[{window_curr_state_str}]",
            "avg": round(avg, 2)
        }

        return Response(response_data, status=status.HTTP_200_OK)
