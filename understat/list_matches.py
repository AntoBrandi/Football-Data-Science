import pandas as pd
import requests
from bs4 import BeautifulSoup
import understat.understat_utilities as un


'''
    LIST MATCHES 
    This functions library is used to extract the list of match IDs that are related
    to a given season for a given series.
    Each match that is played or will in a season is identified by an ID that is 
    needed in order to access the page of that match
'''


# returns the list of match codes for a given series for a given year
def get_matches(series, year):
    # compose the url based on the input values of the function
    url = un.base_url + un.api[0] + '/' + series + '/' + year
    print("Requesting "+url)
    # request the composed url to the server and store it in a variable
    res = requests.get(url)
    # use the beautiful soup library to scrap the website and extract the data
    soup = BeautifulSoup(res.content, "lxml")
    scripts = soup.find_all(un.json_keys[0])
    # the data about the list of matches in a season are stored in the script file
    # in a tag called datesData
    for el in scripts:
        json_matches = []
        if un.json_keys[3] in el.text:
            json_matches.append(el.text.strip())
            json_string_with_data = un.clean_json_data(json_matches)
            # create the pandas data frame
            columns = list(json_string_with_data[0][0].keys())
            values = []
            for i, item in enumerate(json_string_with_data[0]):
                values.append(list(json_string_with_data[0][i].values()))
            df = pd.DataFrame(values, columns= columns)
            df = df[df.isResult == True]
            matches = df['id']
            return matches
    return []
