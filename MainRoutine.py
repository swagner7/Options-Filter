from classes import *
import pandas as pd
import time

inputs_dict = GUI.run_gui() # run GUI to take inputs
td = TDAPI.initialize_api() # initialize TD api

tickers_list = inputs_dict['tickers'] # pull tickers from inputs dict
# tickers_list = ['AAPL', 'IBM']

results = pd.DataFrame() # initalize results df
loop = 1 # initialize loop counter
call_count = 0 # initialize call counter

for j in tickers_list: # loop over tickers
    start_time = time.time()  # record start time
    print(f'\n({loop}/{len(tickers_list)}) Checking for {j} available put options')

    [puts, error_msg] = TDAPI.pull_options(j, inputs_dict['date'], td) # pull available options
    call_count += 1  # increment call counter

    if puts.empty:
        print(error_msg)
    else:
        TDAPI.filter_options(puts, inputs_dict, j)

    # print(call_count/(time.time() - start_time))
    # if (call_count/(time.time()-start_time)) > 1.9 and call_count > 100: # if getting close to api call limit (120/min)
    #     print('Approaching API throttle limit... initiating :30 sleep')
    #     time.sleep(30) # sleep




    if (loop % 119) == 0: # time check to stay under 120 calls/min (API limit)
        print('\nAPI throttle limit reached - initiating 1 min sleep\n')
        t = 60
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print('Sleep time remaining:', timeformat, end='\r')
            time.sleep(1)
            t -= 1

    results = pd.concat([results, puts])  # concatenate all filtered results
    loop += 1 # increment loop counter









end_time = time.time() # record end time