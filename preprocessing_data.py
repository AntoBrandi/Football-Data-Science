import pandas as pd
import config
from pandas import json_normalize
import http.client
import json

connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': config.api_key}

connection.request('GET', '/v2/competitions/SA/scorers', None, headers)
response = json.loads(connection.getresponse().read().decode())
content = json.dumps(response, indent=4, sort_keys=True)

print(response.keys())

# create a pandas dataframe with the response
# df = pd.DataFrame(response['scorers'])

# create another dataset for the others nested json element
scorers = json_normalize(response['scorers'])
print(scorers.head())


