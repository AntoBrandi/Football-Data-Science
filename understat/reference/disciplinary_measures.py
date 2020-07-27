import numpy as np
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup

'''
-- LIVE CODE --
Live code implementation of a web scraping session of the website understat.com
based on the documentation provided in the python script called 'understat_scraper.py'
This code must be cleaned and optimized to retrieve periodically and smoothly the data from
understat.com and store those in a csv local database for consequent analysis and studies
-- LIVE CODE --
'''

# match with yellow cards, red cards and penalties
url = 'https://understat.com/match/7877'
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")
# ok got the egg, let's scrape it
# ok so the data are located in the script tag, let's find all of them bastard
scripts = soup.find_all('script')
json_string_with_data = []
# got it, now the json data are located only under the variable name shotsData and under rostersData
# add those strings to a list of strings
for el in scripts:
    if 'shotsData' in el.text:
        json_string_with_data.append(el.text.strip())
    if 'rostersData' in el.text:
        json_string_with_data.append(el.text.strip())


# still I'm not convinced this gonna work, let's run it and see the output
# for i in json_string_with_data:
#     print(i)
#     print('EOE')
# ok it works but there are even to many data. wtf is webfont and why is it loaded? let's see
# ok it wanted two if conditions on row 18, an or condition was not accepted
# now let's clean the json and make it understandable
data = []
for message in json_string_with_data:
    ind_start = message.index("('")+2
    ind_end = message.index("')")
    json_data = message[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    data.append(json.loads(json_data))
# really i don't know wtf this code up here does, hope it does well
# print(data[0])
# print(data[1])

# looks unbelievable the result, good job guy on the web

# let's make it better anyway and do it looping over strings in json_string_with_data
# ok done, i'm too fucking smart, wish some google recruiter is watching

# now, what the hell is incapsulated in this json message? let's discover it.
# first of all i'm planning to roughly copy paste it into an online json formatter and let's see
# if there is something interesting before have a party
# FUCK YES. In the json file coming from the tag roastersData I can clearly see the indication about the
# yellow card!!!
# for today that's all. Let's continue tomorrow. Super excited.

# from data[0] we can take the information about penalties
# from data[1] we can take information about yellow and red cards
# let's see how the data keys are like
# print(data[0].keys())
# print(data[1].keys())
# ok the keys are just dividing the home (h) and the away team
# save those info in a data set

# also if I only want the disciplinary measures why don't we take the information about
# all the players who played a game?
home = data[1]['h']
away = data[1]['a']
print(home)
print(home.keys())
# save the data of all the players in a match
# let's extract the columns and the values that represent a player in a given match
values = []
for key in home.keys():
    columns = list(home[key].keys())
    values.append(list(home[key].values()))

for key in away.keys():
    values.append(list(away[key].values()))

print(columns)
print(values)
# ok it works, in columns there is the header of the data frame and in the values there is the
# entire data set for the home team. This now has to be done also for the away team
# ok I'm taking all the data of the players in a match. foreach player there is also an information
# about the away or home team. Would be helpful to add another column that says which is the team id
# for the moment is enough
# now let's create a pandas data set with all this data
df = pd.DataFrame(values, columns=columns)
print(df.head())
# let's complete this script
# let's put in a data set all the data related to the message shotsData
# this will contains all interesting information about penalties
events = data[0]
print(events)
print(events.keys())
# ok in this case I'm not going tpo separate the home and the away team
# they are related to the same data flow. I'm only interested in how many penalties have been given
# and to which team
values = []
columns = list(events['h'][0].keys())
print(events['h'])
for key in events.keys():
    for i, event in enumerate(events[key]):
        values.append(list(events[key][i].values()))

print(columns)
print(values)
# ok I know. today i'm a little bit lazy, i'm writing so few comments
# anyway, till this moment everything works quite good, just a little bit of struggle with
# the format of the entries in the events section, anyway it's done. Let's move on with
# the away team.
# I'll try to do that in in only one loop, let's see what happens
# ok that was easy, a nested for loop solves almost everything
# what's next? let's add this data to another pandas data frame
# I think that would be the last duty for this script
df1 = pd.DataFrame(values, columns=columns)
print(df1.head())
# this one was even easier
# OK I do have collected all data for a single match and all of those have been stored in a pandas data frame
# next this script would be a sort of guide to be followed for each match for each season for each series
# so in the next step I'll iterate the previous step for all the matches in a season for all the available seasons

