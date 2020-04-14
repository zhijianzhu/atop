import requests
import json
import pandas as pd

headers = {'Authorization': 'dc70f60f4aab4cfcaeffba24b1ded39d'}

http: // newsapi.org / v2 / top - headlines?sources = google - news & apiKey = dc70f60f4aab4cfcaeffba24b1ded39d

top_headlines_url = 'https://newsapi.org/v2/top-headlines'
everything_news_url = 'https://newsapi.org/v2/everything'
sources_url = 'https://newsapi.org/v2/sources'

headlines_payload = {'category': 'health', 'country': 'us'}
everything_payload = {'q': 'virus', 'language': 'en', 'sortBy': 'popularity'}
sources_payload = {'category': 'general', 'language': 'en', 'country': 'us'}

response = requests.get(
    url=everything_news_url,
    headers=headers,
    params=everything_payload)

df = pd.DataFrame.from_dict(response.json())

pretty_json_output = json.dumps(response.json(), indent=4)
print(pretty_json_output)

# dc70f60f4aab4cfcaeffba24b1ded39d
