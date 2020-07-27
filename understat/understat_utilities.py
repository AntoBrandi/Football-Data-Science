import json

'''
    Collection of variables and constants used in the understat.com website
'''
base_url = 'https://understat.com/'
#leagues = ['La_liga', 'EPL', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL']
leagues = ['Serie_A']
seasons = ['2017']
api = ['league', 'match']
json_keys = ['script', 'rostersData', 'shotsData', 'datesData', 'teamsData', 'playersData']


# magic function that cleans a json string in an understandable format
def clean_json_data(json_message):
    json_message_clean = []
    for message in json_message:
        ind_start = message.index("('")+2
        ind_end = message.index("')")
        json_data = message[ind_start:ind_end]
        json_data = json_data.encode('utf8').decode('unicode_escape')
        json_message_clean.append(json.loads(json_data))
    return json_message_clean
