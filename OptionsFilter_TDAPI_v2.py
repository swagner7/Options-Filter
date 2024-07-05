import json
import os
import datetime as dt
import pandas as pd

def OptionsFilter_TDAPI_v2(ticker,date,c):

    fmt = '%m-%d-%Y' # date format
    date_str = str(date) # cast date to a string
    date_time_obj = dt.datetime.strptime(date_str,fmt) # convert date to datetime object
    date_delta = (date_time_obj - dt.datetime.now()).days + 1

    puts = pd.DataFrame() # initialize dataframe to house puts
    error_encountered = None # initialize error Boolean

    r = c.get_option_chain(ticker, contract_type = c.Options.ContractType.PUT, from_date = date_time_obj, to_date = date_time_obj) # call TD's API to get options data

    # catch errors =========================================================================================================
    read_data = json.load(r) # read in the resultant JSON file

    try:
        if read_data['status'] == 'FAILED':
            error_encountered = True
            error_msg = 'API status failure - no puts available'
        else:
            current_price = float(read_data['underlyingPrice']) # capture current price
            try:
                data_parsed = read_data['putExpDateMap'][str(dt.datetime.strftime(date_time_obj,'%Y-%m-%d') + ':' + str(date_delta))] # first data parse
                error_msg = None
            except:
                error_msg = 'API error - incorrect expiration date'
                error_encountered = True
    except:
        error_encountered = True
        error_msg = 'Unexpected API error - no data returned'
    # =========================================================================================================================================

    if error_encountered is None:
        for a in data_parsed:
            strike_chunk = data_parsed[str(a)][0] # second data parse

            strings = [] # initialize lists for each data point
            strikes = []
            lasts = []
            volumes = []
            ois = []
            bids = []
            asks = []
            currents = []

            strings.append(str(strike_chunk['symbol'])) # append data to empty lists
            strikes.append(float(strike_chunk['strikePrice']))
            lasts.append(float(strike_chunk['last']))
            volumes.append(float(strike_chunk['totalVolume']))
            ois.append(float(strike_chunk['openInterest']))
            bids.append(float(strike_chunk['bid']))
            asks.append(float(strike_chunk['ask']))
            currents.append(current_price)

            dict = {'String':strings,'Strike':strikes,'Last':lasts,'Volume':volumes,'Open Interest':ois,'Bid':bids,'Ask':asks,'Current':currents} # merge lists into dictionary

            df = pd.DataFrame(dict) # merge dictionary into dataframe
            obj = [puts,df] # merge old and new dataframes to an object
            puts = pd.concat(obj,ignore_index = True) # re-assign merged object to dataframe

    return(puts,error_msg)
