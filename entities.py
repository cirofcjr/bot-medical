import os.path
import sys
import requests
import json

DEVELOPER_ACCESS_TOKEN = 'ya29.c.ElpvBtwjb9ri32chMuA2rmkJ86JHttmu-NTSmZLIigeFEfQ_5lzHq9KOHVKl49cx95QSTK8ito-m5A58rpkllRbodBdRDz3tViSCELh8MGiTzw6o-dfnNAMeJYE'


def sending_entities():
    # 1 DEFINE THE URL
    url = "https://dialogflow.googleapis.com/v2/projects/universidade-2a0fa/agent"
    # # 2 DEFINE THE HEADERS
    headers = {'Authorization': 'Bearer '+DEVELOPER_ACCESS_TOKEN,
               'Content-Type': 'application/json'}

    # # 3 CREATE THE DATA
    data = json.dumps({
        "name": "fruit",
        "kind": "KIND_MAP",
        "entries": [
            {
                "synonyms": ["apple", "red apple"],
                "value": "apple"
            },
            {
                "value": "banana"
            }
        ]
    })

   # 4 MAKE THE REQUEST
    response = requests.get(url, headers=headers)
    # , headers=headers, data=data)
    print(response.json)


sending_entities()
