import json
import requests

def apollo_link(domain, key):
    url = "https://api.apollo.io/api/v1/organizations/enrich?domain=" + domain

    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": key
    }

    response = requests.get(url, headers=headers)

    data = json.loads(response.text).get("organization")
    idd = data.get("id")

    return "https://app.apollo.io/#/organizations/" + idd
