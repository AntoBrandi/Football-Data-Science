import pandas as pd
import time
import understat.understat_utilities as un
import understat.list_matches as lm
import understat.match_details as md

'''
    FOOTBALL DATA COLLECTOR
    Script that collects data from the website www.understat.com and saves those
    in local csv storage for further analysis
'''

# create the data frame that will contain all the data that are needed
shotsDF = pd.DataFrame()
roastersDF = pd.DataFrame()
# track the number of iterations needed to complete the extraction in order to give a feedback to the user
n_iterations = len(un.leagues)*len(un.seasons)*380
counter = 0

for league in un.leagues:
    for season in un.seasons:
        matches = lm.get_matches(league, season)
        for match in matches:
            shotsData, roastersData = md.get_match_details(match, season, league)
            shotsDF = shotsDF.append(shotsData, ignore_index=True)
            roastersDF = roastersDF.append(roastersData, ignore_index=True)
            counter += 1
            print('iteration ', counter, 'of ', n_iterations, ' match', match)
            time.sleep(1)
print(shotsDF.head())
print(roastersDF.head())
# save this data frames in a csv file
shotsDF.to_csv('shots_df.csv')
roastersDF.to_csv('roasters_df.csv')

