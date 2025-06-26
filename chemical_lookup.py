import requests
import urllib3

# Disable SSL warnings (for local testing only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_pubchem_image(chemical_name):
    # Auto-suggestion: if endswith 'ate', try replacing 'ate' with 'ole' first
    if chemical_name.endswith("ate"):
        suggested_name = chemical_name[:-3] + "ole"
        print(f"Trying suggested name first: {suggested_name}")
        cid, image_url, source = fetch_pubchem_image_simple(suggested_name)
        if cid:
            return cid, image_url, f"PubChem (suggested: {suggested_name})"
        # If suggestion fails, fallback to original name search
        print(f"Suggested name failed, trying original name: {chemical_name}")
        cid, image_url, source = fetch_pubchem_image_simple(chemical_name)
        if cid:
            return cid, image_url, source
    else:
        # Normal flow
        return fetch_pubchem_image_simple(chemical_name)
    return None, "Not found", None

def fetch_pubchem_image_simple(name):
    # Try name search
    url_name = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/JSON"
    r = requests.get(url_name, verify=False)
    if r.status_code == 200 and 'IdentifierList' in r.json():
        cid = r.json()['IdentifierList']['CID'][0]
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
        return cid, image_url, "PubChem"
    # Try synonym search
    url_syn = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/synonym/{name}/cids/JSON"
    r_syn = requests.get(url_syn, verify=False)
    if r_syn.status_code == 200 and 'IdentifierList' in r_syn.json():
        cid = r_syn.json()['IdentifierList']['CID'][0]
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
        return cid, image_url, "PubChem"
    # Fallback cactus
    cactus_url = f"https://cactus.nci.nih.gov/chemical/structure/{name}/image"
    r_cactus = requests.get(cactus_url, verify=False)
    if r_cactus.status_code == 200:
        return "CACTUS", cactus_url, "Cactus"
    return None, "Not found", None
