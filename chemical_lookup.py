import requests
import urllib3

# Disable SSL warnings (only for local testing; remove in production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_pubchem_image(chemical_name):
    print(f"[DEBUG] Received input: {chemical_name}")

    # Auto-suggestion: if ends with 'ate', try 'ole' variant first
    if chemical_name.endswith("ate"):
        suggested_name = chemical_name[:-3] + "ole"
        print(f"[DEBUG] Trying suggested name: {suggested_name}")
        cid, image_url, source = fetch_pubchem_image_simple(suggested_name)
        if cid:
            print(f"[DEBUG] Found CID with suggested name: {cid}")
            return cid, image_url, f"PubChem (suggested: {suggested_name})"
        else:
            print(f"[DEBUG] Suggested name failed, trying original name: {chemical_name}")
            cid, image_url, source = fetch_pubchem_image_simple(chemical_name)
            if cid:
                print(f"[DEBUG] Found CID with original name: {cid}")
                return cid, image_url, source
    else:
        cid, image_url, source = fetch_pubchem_image_simple(chemical_name)
        if cid:
            print(f"[DEBUG] Found CID with original name: {cid}")
            return cid, image_url, source

    print("[DEBUG] Chemical not found anywhere")
    return None, "Not found", None

def fetch_pubchem_image_simple(name):
    # Try PubChem name search
    url_name = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/JSON"
    print(f"[DEBUG] PubChem name search URL: {url_name}")
    r = requests.get(url_name, verify=False)
    print(f"[DEBUG] PubChem name search status: {r.status_code}")
    if r.status_code == 200:
        json_data = r.json()
        if 'IdentifierList' in json_data and 'CID' in json_data['IdentifierList']:
            cid = json_data['IdentifierList']['CID'][0]
            image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
            return cid, image_url, "PubChem"

    # Try PubChem synonym search
    url_syn = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/synonym/{name}/cids/JSON"
    print(f"[DEBUG] PubChem synonym search URL: {url_syn}")
    r_syn = requests.get(url_syn, verify=False)
    print(f"[DEBUG] PubChem synonym search status: {r_syn.status_code}")
    if r_syn.status_code == 200:
        json_data = r_syn.json()
        if 'IdentifierList' in json_data and 'CID' in json_data['IdentifierList']:
            cid = json_data['IdentifierList']['CID'][0]
            image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
            return cid, image_url, "PubChem"

    # Fallback to NCI Cactus resolver (image only)
    cactus_url = f"https://cactus.nci.nih.gov/chemical/structure/{name}/image"
    print(f"[DEBUG] Cactus resolver URL: {cactus_url}")
    r_cactus = requests.get(cactus_url, verify=False)
    print(f"[DEBUG] Cactus resolver status: {r_cactus.status_code}")
    if r_cactus.status_code == 200:
        return "CACTUS", cactus_url, "Cactus"

    return None, "Not found", None
