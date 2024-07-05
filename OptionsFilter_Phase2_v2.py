import pandas as pd
import os
import datetime as dt
from OptionsFilter_TDAPI_v2 import OptionsFilter_TDAPI_v2
from tda import auth, client
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import time

def OptionsFilter_Phase2_v2(date):
# find support ==============================================================================================================================
    def find_support(ticker):
        r = c.get_price_history(ticker, frequency_type=c.PriceHistory.FrequencyType.DAILY, frequency=c.PriceHistory.Frequency.DAILY, period_type=c.PriceHistory.PeriodType.YEAR, period=c.PriceHistory.Period.ONE_YEAR)

        read_data = json.load(r)
        first_parse = read_data['candles']

        closes = []
        for j in range(len(first_parse)):
            closes.append(float(first_parse[j]['close']))

        closes_array = np.array(closes)
        support_points = list(argrelextrema(closes_array, np.less, order = 20)[0])
        support_levels = closes_array[support_points]

        if len(support_levels) > 0:
            most_recent_support = support_levels[len(support_levels)-1]
            most_recent_support_point = len(closes) - support_points[len(support_points)-1]
        else:
            print('Not enough',ticker,'data to calculate support levels')
            most_recent_support = np.nan
            most_recent_support_point = np.nan

        # plt.plot(closes)
        # plt.title(ticker + ' Price History')
        # plt.hlines(support_levels,support_points,len(closes))
        # plt.xlabel('Days from one year ago')
        # plt.show()
        return(most_recent_support,most_recent_support_point)
    # =======================================================================================================================================
    viable_options = pd.read_csv('OptionsFilterResults_' + date + '.csv') # read in results csv

    redirect_uri = 'https://localhost/test'
    api_key = 'FUVZJSZJQI4DR8HPQKEVJGLSLBQJXPMG'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    token_path = str(dir_path.replace('\\','/') + '/td_state.json')
    c = auth.client_from_token_file(token_path, api_key)


    pull_tickers = []
    for row in range(0,len(viable_options.index)):
        pull_tickers.append(viable_options['String'][row].split('_')[0]) # extract ticker from contract string

    phase2_tickers = []
    for i in pull_tickers:
        if i not in phase2_tickers:
            phase2_tickers.append(i) # remove duplicates from list of tickers

    phase2_df = pd.DataFrame(phase2_tickers, columns = ['Ticker'])

    support = []
    ago = []
    loop = 1
    for row in range(0,len(phase2_df.index)):
        ticker = phase2_df['Ticker'][row]

        [most_recent_support,most_recent_support_point] = find_support(ticker)
        support.append(most_recent_support)
        ago.append(most_recent_support_point)

        if np.isnan(most_recent_support) == False:
            print('Most recent',ticker,'support level is',most_recent_support,'which occured',most_recent_support_point,'days ago')

        if (loop % 110) == 0:
            print('\nAPI throttle limit reached - initiating 1 min sleep\n')
            t = 60
            while t:
                mins, secs = divmod(t, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                print('Sleep time remaining:', timeformat, end='\r')
                time.sleep(1)
                t -= 1
        loop += 1

    phase2_df['Support'] = support
    phase2_df['Days Ago'] = ago

    addon_df = pd.DataFrame()
    addon_df['String'] = viable_options['String']
    addon_support = []
    addon_ago = []
    for row in range(0,len(viable_options.index)):
        ticker = viable_options['String'][row].split('_')[0]

        pull_support = (phase2_df.loc[phase2_df['Ticker'] == ticker]['Support']).values[0]
        pull_daysago = (phase2_df.loc[phase2_df['Ticker'] == ticker]['Days Ago']).values[0]
        addon_support.append(pull_support)
        addon_ago.append(pull_daysago)

    addon_df['Support'] = addon_support
    addon_df['Days Ago'] = addon_ago

    viable_options = viable_options.merge(addon_df, on = 'String')
    viable_options['Support Delta (%)'] = round(((viable_options['Strike'] - viable_options['Support']) / viable_options['Strike']) * 100,3)

    return(viable_options)

#asdf
