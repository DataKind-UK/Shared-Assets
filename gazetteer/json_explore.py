# Python code that takes a geoJSON output from the API and strips out all the unnecessary stuff. What's in this result should validate as good geoJSON'

import json
from pprint import pprint

with open('19422598.json') as data_file:    
    data = json.load(data_file)

pprint(data['data'][0]["inspire_poly"])