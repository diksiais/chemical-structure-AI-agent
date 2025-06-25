import requests
import urllib3

# Disable SSL warnings (safe for local testing)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_pubchem_image(chemical_name):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/cids/JSON"
    r = requests.get(url, verify=False)  # <-- ignore SSL cert errors
    if r.status_code != 200 or 'IdentifierList' not in r.json():
        return None, "Not found"
    cid = r.json()['IdentifierList']['CID'][0]
    image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
    return cid, image_url
