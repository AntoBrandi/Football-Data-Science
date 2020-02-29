import pandas as pd
import config
from pandas import json_normalize
import http.client
import json
import time

'''
Script for recursively query the API of the website api.football-data.org in order to get 
the list of players and staff of each team and save it to a csv file. This is due in order to avoid the limitation
given from the website

This script fills the file called teams_df.csv
'''
connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': config.api_key}

# load the matched_d.csv and for each team, query the database
matches = pd.read_csv('matches_df.csv')
homeTeams = []
for index, row in matches.iterrows():
    homeTeams.append(row['homeTeam.id'])

# reduce the list to distinct elements
teams = set(homeTeams)
print(teams)

# for each team send a query to the data source and store the data into a csv file
for x, team in enumerate(teams):
    # request the teams lineup
    connection.request('GET', '/v2/teams/'+str(team), None, headers)
    response = json.loads(connection.getresponse().read().decode())
    # make the json look nicer
    content = json.dumps(response, indent=4, sort_keys=True)
    print(content)

    # create a data set for the top scorer
    squad = json_normalize(response)
    # if is the first entry, create and write on the cs file
    if x == 0:
        # export the data set to csv, useful for the limitation of the API requests
        squad.to_csv('teams_df.csv')
    # is not the first entry, just append the data set
    else:
        squad.to_csv('teams_df.csv', mode='a', header=False)

    # wait before sending a new request ( max 10 in 60s)
    # make 6 requests every minute
    time.sleep(10)



