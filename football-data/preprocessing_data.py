import pandas as pd
import config
from pandas import json_normalize
import http.client
import json
import os
''' Italian A series related Data
Creation of a data set that retrieve information about italian top football series including top scorers,
historical results, historical scores etc.
This data set will be the starting point for making prediction about both scores and results
'''
connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': config.api_key}

# # request the top 10 scorers of italian A series
# connection.request('GET', '/v2/competitions/SA/scorers?season=2018', None, headers)
# response = json.loads(connection.getresponse().read().decode())
# # make the json look nicer
# content = json.dumps(response, indent=4, sort_keys=True)
#
# # create a data set for the top scorer
# scorers = json_normalize(response['scorers'])
# print(scorers)

# # request a match detail
# connection.request('GET', '/v2/competitions/SA/matches?season=2018', None, headers)
# response = json.loads(connection.getresponse().read().decode())
# # make the json look nicer
# content = json.dumps(response, indent=4, sort_keys=True)
#
# print(content)
#
# # create a data set for the matches occurred this season for the italian championship
# matches = json_normalize(response['matches'])
# print(matches.head())
#
# # export the data set to csv, useful for the limitation of the API requests
# matches.to_csv(r'C:\Users\anton\Documents\Python Scripts\SportNN\FootballNN\matches_df.csv')


# different way for request a match detail in a given period of time
# connection.request('GET', '/v2/matches?competitions=SA&dateFrom=2019-08-20&dateTo=2019-08-30', None, headers)
# response = json.loads(connection.getresponse().read().decode())
# # make the json look nicer
# content = json.dumps(response, indent=4, sort_keys=True)
#
# print(content)
#
# # create a data set for the matches occurred this season for the italian championship
# matches = json_normalize(response['matches'])
# print(matches.head())


# # request the teams lineup
# connection.request('GET', '/v2/teams/67', None, headers)
# response = json.loads(connection.getresponse().read().decode())
# # make the json look nicer
# content = json.dumps(response, indent=4, sort_keys=True)
# print(content)
#
# # create a data set for the top scorer
# matches = json_normalize(response['squad'])
# print(matches.head())


