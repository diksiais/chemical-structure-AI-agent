import requests
import urllib3

# Disable SSL warnings (for local testing only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_pubchem_image(chemical_name):
    # First try: search by name
    url_name = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/cids/JSON"
    r = requests.get(url_name, verify=False)
    if r.status_code == 200 and 'IdentifierList' in r.json():
        cid = r.json()['IdentifierList']['CID'][0]
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
        return cid, image_url

    # Second try: search by synonyms
    url_syn = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/synonym/{chemical_name}/cids/JSON"
    r_syn = requests.get(url_syn, verify=False)
    if r_syn.status_code == 200 and 'IdentifierList' in r_syn.json():
        cid = r_syn.json()['IdentifierList']['CID'][0]
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
        return cid, image_url

    return None, "Not found"
