import requests
import urllib3

# Disable SSL warnings (for local testing only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_pubchem_image(chemical_name):
    # First try: search by name in PubChem
    url_name = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/cids/JSON"
    r = requests.get(url_name, verify=False)
    if r.status_code == 200 and 'IdentifierList' in r.json():
        cid = r.json()['IdentifierList']['CID'][0]
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
        return cid, image_url, "PubChem"

    # Second try: search by synonym in PubChem
    url_syn = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/synonym/{chemical_name}/cids/JSON"
    r_syn = requests.get(url_syn, verify=False)
    if r_syn.status_code == 200 and 'IdentifierList' in r_syn.json():
        cid = r_syn.json()['IdentifierList']['CID'][0]
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
        return cid, image_url, "PubChem"

    # Auto-suggestion: try correcting common endings like "-ate" to "-ole"
    if chemical_name.endswith("ate"):
        suggested_name = chemical_name.replace("ate", "ole")
        url_suggest = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{suggested_name}/cids/JSON"
        r_suggest = requests.get(url_suggest, verify=False)
        if r_suggest.status_code == 200 and 'IdentifierList' in r_suggest.json():
            cid = r_suggest.json()['IdentifierList']['CID'][0]
            image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
            return cid, image_url, f"PubChem (suggested: {suggested_name})"

    # Third try: fallback to NCI Cactus structure resolver
    cactus_url = f"https://cactus.nci.nih.gov/chemical/structure/{chemical_name}/image"
    r_cactus = requests.get(cactus_url, verify=False)
    if r_cactus.status_code == 200:
        return "CACTUS", cactus_url, "Cactus"

    return None, "Not found", None
