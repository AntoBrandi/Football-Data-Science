import pandas as pd
import requests
from bs4 import BeautifulSoup
import understat.understat_utilities as un

'''
    MATCH DETAIL
    This function library is used to extract a match feature and details
    given the match ID.
    The extracted details are mainly the disciplinary measures taken in a match
    and the penalties eventually given in the match  
'''


def get_match_details(match_id, season, serie):
    # compose the url based on the input of the function
    url = un.base_url + un.api[1] + '/' + match_id
    print("Requesting " + url)
    # request the composed url to the server and store it in a variable
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    # find the data into the web page and store those in cleaned json variables
    scripts = soup.find_all(un.json_keys[0])
    json_string_with_data = []
    for el in scripts:
        if un.json_keys[2] in el.text:
            json_string_with_data.append(el.text.strip())
        if un.json_keys[1] in el.text:
            json_string_with_data.append(el.text.strip())
    # clean the json data
    data = un.clean_json_data(json_string_with_data)
    print(data)

    # extract the data from the json string message
    # extract the data for the disciplinary measures
    values = []
    for key in data[1]['h'].keys():
        columns = list(data[1]['h'][key].keys())
        values.append(list(data[1]['h'][key].values()))
    for key in data[1]['a'].keys():
        values.append(list(data[1]['a'][key].values()))
    # create a data frame for the current match shotsData
    # Add tre columns to each data frame regarding the
    # match id, season year and season name/code
    shotsData = pd.DataFrame(values, columns=columns)
    shotsData.insert(0, 'match_id', match_id)
    shotsData.insert(1, 'season_year', season)
    shotsData.insert(2, 'championship_name', serie)
    # extract also the data for the penalties
    values = []
    columns = list(data[0]['h'][0].keys())
    for key in data[0].keys():
        for i, event in enumerate(data[0][key]):
            values.append(list(data[0][key][i].values()))
    # create a partial data frame for the current match roastersData
    roastersData = pd.DataFrame(values, columns=columns)
    roastersData.insert(1, 'championship_name', serie)

    return shotsData, roastersData
