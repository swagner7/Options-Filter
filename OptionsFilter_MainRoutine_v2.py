import time
from OptionsFilter_TDAPI_v2 import OptionsFilter_TDAPI_v2
import os
import pandas as pd
from tda import auth, client
import json
import requests
import datetime as dt
from OptionsFilter_Phase2_v2 import OptionsFilter_Phase2_v2

def OptionsFilter_MainRoutine_v2(date,tickers_list,bid_flag,prem_flag,delta_flag,strike_flag,volume_flag,bid_filter,prem_filter,delta_filter,strike_filter,volume_filter):
    t1 = time.time()

    # connect to TD api ========================================================================================================================================================
    redirect_uri = 'https://localhost/test'
    api_key = 'FUVZJSZJQI4DR8HPQKEVJGLSLBQJXPMG'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    token_path = str(dir_path.replace('\\','/') + '/td_state.json')

    # token_path = 'C:/Users/swagner/PythonVENV/env/Projects/td_state.json'

    try: # try getting authentication from JSON file
        c = auth.client_from_token_file(token_path, api_key)
    except FileNotFoundError:
        from selenium import webdriver # import web crawling library
        with webdriver.Chrome() as driver:
            c = auth.client_from_login_flow(driver, api_key, redirect_uri, token_path) # if no JSON file exists, redirct to client login

    # filter options ===========================================================================================================================================================
    contracts = 1
    results = pd.DataFrame() # initialize results df

    # tickers_list = ['AAPL','SIEB','IBM']

    loop = 1
    for j in tickers_list:
        j = list([val for val in j if val.isalpha()])
        j = "".join(j)
        j = j.strip()
        print(f'\n({loop}/{len(tickers_list)}) Checking for {j} available put options')

        [puts,error_msg] = OptionsFilter_TDAPI_v2(j,date,c) # call API
        if puts.empty:
            print(error_msg)
        else:
            print('\nPuts found!')
            puts['Premium'] = round(puts['Last']*contracts*100,3) # add Premium column
            puts['VaR'] = round(puts['Strike']*contracts*100,3) # add VaR column
            puts['Premium/VaR (%)'] = round(100*puts['Premium']/puts['VaR'],3) # add Premium/VaR column
            puts['Delta (%)'] = round(100*(puts['Current'] - puts['Strike'])/puts['Current'],3) # add Delta column

            if bid_flag == 1:
                puts = puts[puts['Bid'] > bid_filter]

            if prem_flag == 1:
                puts = puts[puts['Premium/VaR (%)'] > prem_filter]

            if delta_flag == 1:
                puts = puts[puts['Delta (%)'] > delta_filter]

            if strike_flag == 1:
                puts = puts[puts['Strike'] > strike_filter]

            if volume_flag == 1:
                puts = puts[puts['Volume'] > volume_filter]

            if puts.empty:
                print(f'\nNo viable {j} puts')
            else:
                print('\nViable puts:')
                print(puts)

        results = pd.concat([results,puts]) # concatenate all filtered results

        if (loop % 119) == 0:
            print('\nAPI throttle limit reached - initiating 1 min sleep\n')
            t = 60
            while t:
                mins, secs = divmod(t, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                print('Sleep time remaining:', timeformat, end='\r')
                time.sleep(1)
                t -= 1

        loop += 1

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    print('\n--------------------------------------------------------------------------------------------------------------')
    if results.empty:
        print('No vialbe puts were found for',str(date))
    else:
        results = results.reset_index(drop=True)
        pd.set_option('display.max_rows', None)
        results = results.sort_values('Premium/VaR (%)',ascending = False)

        print("\n" + str(len(results['String'])) + " viable put options found on exercise date " + str(date) + ":\n")
        print(results)
        t2 = time.time()
        print('\nStopwatch: ' + str(round(t2-t1,3)) + ' seconds, ' + str(round((t2-t1)/len(tickers_list),3)) + ' sec/ticker')

        results.to_csv('OptionsFilterResults_' + date + '.csv',sep=',',index = False) # output csv file

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    print('\n========================================================================================================================================\n')
    print('Initiating Phase 2')
    print('\n=========================================================================================================================================\n')


    results_2 = OptionsFilter_Phase2_v2(date)
    print('\n',results_2)
    results_2.to_csv('OptionsFilter_Phase2_Results_' + date + '.csv',sep=',',index = False) # output csv file
