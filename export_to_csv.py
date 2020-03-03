import pandas as pd
import config
from pandas import json_normalize
import http.client
import time
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
    responseMatches = json.loads(connection.getresponse().read().decode())
    # make the json look nicer
    # only for debug
    # content = json.dumps(response, indent=4, sort_keys=True)
    # print(content)
    # request the list of top scorer
    connection.request('GET', '/v2/competitions/SA/scorers?season='+str(year), None, headers)
    responseScorers = json.loads(connection.getresponse().read().decode())
    # request the standing
    connection.request('GET', '/v2/competitions/SA/standings?season='+str(year), None, headers)
    responseStandings = json.loads(connection.getresponse().read().decode())

    # create a data set for the matches occurred this season for the italian championship
    matches = json_normalize(responseMatches['matches'])
    # create a data set for the scorers occurred this season
    scorers = json_normalize(responseScorers)
    # create a data set for the standings
    standings = json_normalize(responseStandings)

    # if is the first entry, create and write on the cs file
    if year == START_YEAR:
        # export the data set to csv, useful for the limitation of the API requests
        matches.to_csv('matches_df.csv')
        scorers.to_csv('scorers_df.csv')
        standings.to_csv('standings_df.csv')

    # is not the first entry, just append the data set
    else:
        matches.to_csv('matches_df.csv', mode='a', header=False)
        scorers.to_csv('scorers_df.csv', mode='a', header=False)
        standings.to_csv('standings_df.csv', mode='a', header=False)

    year += 1


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
    time.sleep(10)
