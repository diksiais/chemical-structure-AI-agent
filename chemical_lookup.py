import requests
import urllib3

# Disable SSL warnings (for local testing only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_pubchem_image(chemical_name):
    print(f"Searching for: {chemical_name}")
    
    # First try: search by name in PubChem
    url_name = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/cids/JSON"
    r = requests.get(url_name, verify=False)
    print(f"PubChem name search status: {r.status_code}")
    if r.status_code == 200 and 'IdentifierList' in r.json():
        cid = r.json()['IdentifierList']['CID'][0]
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
        print(f"Found in PubChem name search: CID={cid}")
        return cid, image_url, "PubChem"

    # Second try: search by synonym in PubChem
    url_syn = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/synonym/{chemical_name}/cids/JSON"
    r_syn = requests.get(url_syn, verify=False)
    print(f"PubChem synonym search status: {r_syn.status_code}")
    if r_syn.status_code == 200 and 'IdentifierList' in r_syn.json():
        cid = r_syn.json()['IdentifierList']['CID'][0]
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
        print(f"Found in PubChem synonym search: CID={cid}")
        return cid, image_url, "PubChem"

    # Auto-suggestion: try correcting common endings like "-ate" to "-ole"
    if chemical_name.endswith("ate"):
        suggested_name = chemical_name[:-3] + "ole"  # safer replacement
        print(f"Trying suggested name: {suggested_name}")
        url_suggest = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{suggested_name}/cids/JSON"
        r_suggest = requests.get(url_suggest, verify=False)
        print(f"PubChem suggested name search status: {r_suggest.status_code}")
        if r_suggest.status_code == 200 and 'IdentifierList' in r_suggest.json():
            cid = r_suggest.json()['IdentifierList']['CID'][0]
            image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
            print(f"Found in PubChem suggested name search: CID={cid}")
            return cid, image_url, f"PubChem (suggested: {suggested_name})"

    # Third try: fallback to NCI Cactus structure resolver
    cactus_url = f"https://cactus.nci.nih.gov/chemical/structure/{chemical_name}/image"
    r_cactus = requests.get(cactus_url, verify=False)
    print(f"Cactus search status: {r_cactus.status_code}")
    if r_cactus.status_code == 200:
        print(f"Found in Cactus resolver")
        return "CACTUS", cactus_url, "Cactus"

    print("Chemical not found anywhere")
    return None, "Not found", None
