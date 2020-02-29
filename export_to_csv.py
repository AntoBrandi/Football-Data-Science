import pandas as pd
import config
from pandas import json_normalize
import http.client
import json

'''
Script for recursively query the API of the website api.football-data.org in order to get 
the list of matches of each year and save it to a csv file. This is due in order to avoid the limitation
given from the website

This script fills the file called matches_df.csv
'''
connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': config.api_key}
START_YEAR = 2018
END_YEAR = 2019


# request the match detail for the last available seasons
year = START_YEAR
while year <= END_YEAR:
    # request a match detail
    connection.request('GET', '/v2/competitions/SA/matches?season='+str(year), None, headers)
    response = json.loads(connection.getresponse().read().decode())
    # make the json look nicer
    content = json.dumps(response, indent=4, sort_keys=True)
    print(content)

    # create a data set for the matches occurred this season for the italian championship
    matches = json_normalize(response['matches'])

    # if is the first entry, create and write on the cs file
    if year == START_YEAR:
        # export the data set to csv, useful for the limitation of the API requests
        matches.to_csv('matches_df.csv')
    # is not the first entry, just append the data set
    else:
        matches.to_csv('matches_df.csv', mode='a', header=False)

    year += 1
