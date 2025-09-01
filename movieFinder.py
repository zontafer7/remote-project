import requests

class MovieFinder:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.baseUrl = 'https://api.themoviedb.org/3'

    def search(self, query, type='multi',page=1):
        url = f"{self.baseUrl}/search/{type}"
        params = {
            "api_key": self.apiKey,
            "query": query,
            "language": "en-US",
            "page": page,
            "include_adult": False
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"TMDB API Error: {response.status_code}")
        data = response.json()
        return data.get("results", [])

    def getDetails(self, movieID):
        url = f"{self.baseUrl}/movie/{movieID}"
        params = {
            "api_key" : self.apiKey,
            "language": "en-US"
        }
