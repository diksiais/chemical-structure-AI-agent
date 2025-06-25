import requests
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def search_papers(query, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,authors,year,url,abstract"
    r = requests.get(url, verify=False)  # Bypass SSL certificate error
    if r.status_code == 200:
        return r.json().get('data', [])
    return []
