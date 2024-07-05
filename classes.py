class GUI:
    def run_gui():
        import tkinter as tk
        master = tk.Tk() # start main tkinter loop
        master.title('Options Filter GUI')

        # action functions ------------------------------------------------------------------
        def toggle():
            '''
            use
            t_btn.config('text')[-1]
            to get the present state of the toggle button
            '''
            if t_btn.config('text')[-1] == 'True':
                t_btn.config(text='False')
            else:
                t_btn.config(text='True')

            return()

        def run_calendar():
            from tkcalendar import Calendar, DateEntry
            def confirm_selection():
                cal_date = cal.get_date()
                cal_entry.delete(0, 'end') # clear entry box
                cal_entry.insert(0, str(cal_date)) # insert date into entry box
                top.destroy() # destroy calendar
                return()

            top = tk.Toplevel(master) # initialize a top level root
            cal = Calendar(top, selectmode = 'day', date_pattern = 'mm-dd-yyyy') # call new calendar
            cal.pack(fill = "both", expand = True)
            tk.Button(top, text = "Select", command = confirm_selection).pack() # create "confirm" button
            return()

        def run_selected():
            global inputs_dict

            # pull checkbox flags to assign to filter flags
            bid_flag = True if bid_entry.get() == 1 else False
            premvar_flag = True if premvar_entry.get() == 1 else False
            delta_flag = True if delta_entry.get() == 1 else False
            strike_flag = True if strike_entry.get() == 1 else False
            volume_flag = True if volume_entry.get() == 1 else False

            # pull entry box values to assign to variables
            date = str(cal_entry.get())
            tickers_list = str(tickers_entry.get()).upper().split(',') # split list on , and make all uppercase
            bid_filter = float(bid_box.get())
            premvar_filter = float(premvar_box.get())
            delta_filter = float(delta_box.get())
            strike_filter = float(strike_box.get())
            volume_filter = float(volume_box.get())

            # pack input values into dict
            inputs_dict = {'date': date, 'tickers': tickers_list, 'bid flag': bid_flag, 'bid filter': bid_filter, 'premvar flag': premvar_flag, 'premvar filter': premvar_filter, 'delta flag': delta_flag,
                           'delta filter': delta_filter, 'strike flag': strike_flag, 'strike filter': strike_filter, 'volume flag': volume_flag, 'volume_filter': volume_filter}

            print(f'Tickers chosen: {tickers_list}')
            print(f'Expiration date chosen: {date}')
            master.quit()
            return(inputs_dict)

        def run_all():
            import requests
            import pandas as pd
            global inputs_dict

            # pull checkbox flags to assign to filter flags
            bid_flag = True if bid_entry.get() == 1 else False
            premvar_flag = True if premvar_entry.get() == 1 else False
            delta_flag = True if delta_entry.get() == 1 else False
            strike_flag = True if strike_entry.get() == 1 else False
            volume_flag = True if volume_entry.get() == 1 else False

            # pull entry box values to assign to variables
            date = str(cal_entry.get())
            tickers_list = str(tickers_entry.get()).upper().split(',') # split list on , and make all uppercase
            bid_filter = float(bid_box.get())
            premvar_filter = float(premvar_box.get())
            delta_filter = float(delta_box.get())
            strike_filter = float(strike_box.get())
            volume_filter = float(volume_box.get())

            print(f'Expiration date chosen: {date}')
            print('Running all tickers')

            print('Pulling list of tickers')
            headers = {
                'authority': 'api.nasdaq.com',
                'accept': 'application/json, text/plain, */*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'origin': 'https://www.nasdaq.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.nasdaq.com/',
                'accept-language': 'en-US,en;q=0.9',
            }

            params = (
                ('tableonly', 'true'),
                ('limit', '25'),
                ('offset', '0'),
                ('download', 'true'),
            )

            r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers = headers, params = params)
            data = r.json()['data']
            tickers_list = pd.DataFrame(data['rows'], columns = data['headers'])

            tickers_list = [item.strip() for item in list(tickers_list['symbol']) if item.find('^') == -1 and item.find('/') == -1]  # filter out tickers with '^' or '/'

            # pack input values into dict
            inputs_dict = {'date': date, 'tickers': tickers_list, 'bid flag': bid_flag, 'bid filter': bid_filter, 'premvar flag': premvar_flag, 'premvar filter': premvar_filter, 'delta flag': delta_flag,
                           'delta filter': delta_filter, 'strike flag': strike_flag, 'strike filter': strike_filter, 'volume flag': volume_flag, 'volume filter': volume_filter}

            master.quit()
            return(inputs_dict)
        # ----------------------------------------------------------------------------------
        # create calendar entry
        tk.Button(master, text = 'Open Calendar', command  = run_calendar).grid(row = 2, column = 1) # button
        tk.Label(master, text = 'Required:').grid(row = 0) # label
        tk.Label(master, text = 'Expiration Date (mm-dd-yyyy)').grid(row = 1) # label
        cal_entry = tk.Entry(master) # entry box
        cal_entry.grid(row = 1, column = 1)  # place on grid

        # create optional tickers entry
        tk.Label(master, text = 'Optional:').grid(row = 3) # label
        tk.Label(master, text = 'Tickers (separate with comma)').grid(row = 4) # label
        tickers_entry = tk.Entry(master) # entry box
        tickers_entry.grid(row = 4, column = 1) # place on grid

        # create action buttons
        tk.Button(master, text='Run All Tickers', command = run_all).grid(row=7, column=0)
        tk.Button(master, text='Run Selected Tickers', command = run_selected).grid(row=7, column=1)
        tk.Button(master, text='Quit', command = master.quit).grid(row=7, column=3)
        tk.Button(text = 'Puts', command = toggle).grid(row=7, column=4)

        # create filter checkboxes ------------------------------------------------------
        tk.Label(master, text = 'Choose filters:').grid(row = 0, column = 2) # label
        # bid
        bid_box = tk.Entry(master) # entry box
        bid_box.insert(0, 1) # insert value
        bid_box.grid(row = 1, column = 3)  # place on grid
        bid_entry = tk.IntVar() # initialize variable for entry
        bid_entry.set(1) # set variable
        tk.Checkbutton(master, text = "Bid > ", variable = bid_entry, onvalue = 1, offvalue = 0).grid(row = 1, column = 2) # checkbox

        # premium/var
        tk.Label(master, text='%').grid(row=2, column=4) # % label
        premvar_box = tk.Entry(master) # entry box
        premvar_box.insert(0, 1) # insert value
        premvar_box.grid(row = 2, column = 3)  # place on grid
        premvar_entry = tk.IntVar() # initialize variable for entry
        premvar_entry.set(1) # set variable
        tk.Checkbutton(master, text = "Premium/VAR > ", variable = premvar_entry, onvalue = 1, offvalue = 0).grid(row = 2, column = 2) # checkbox

        # delta
        tk.Label(master, text='%').grid(row=3, column=4) # % label
        delta_box = tk.Entry(master) # entry box
        delta_box.insert(0, 10) # insert value
        delta_box.grid(row = 3, column = 3)  # place on grid
        delta_entry = tk.IntVar() # initialize variable for entry
        delta_entry.set(1) # set variable
        tk.Checkbutton(master, text = "Delta > ", variable = delta_entry, onvalue = 1, offvalue = 0).grid(row = 3, column = 2) # checkbox

        # strike
        strike_box = tk.Entry(master) # entry box
        strike_box.insert(0, 10) # insert value
        strike_box.grid(row = 4, column = 3)  # place on grid
        strike_entry = tk.IntVar() # initialize variable for entry
        strike_entry.set(1) # set variable
        tk.Checkbutton(master, text = "Strike > ", variable = strike_entry, onvalue = 1, offvalue = 0).grid(row = 4, column = 2) # checkbox

        # volume
        volume_box = tk.Entry(master) # entry box
        volume_box.insert(0, 5) # insert value
        volume_box.grid(row = 5, column = 3)  # place on grid
        volume_entry = tk.IntVar() # initialize variable for entry
        volume_entry.set(1) # set variable
        tk.Checkbutton(master, text = "Volume > ", variable = volume_entry, onvalue = 1, offvalue = 0).grid(row = 5, column = 2) # checkbox

        tk.mainloop() # close main tkinter loop
        return(inputs_dict)


class TDAPI:
    def initialize_api():
        import os
        redirect_uri = 'https://localhost/test'
        api_key = 'FUVZJSZJQI4DR8HPQKEVJGLSLBQJXPMG'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        token_path = str(dir_path.replace('\\', '/') + '/td_state.json')

        try:  # try getting authentication from JSON file
            from tda import auth, client
            td = auth.client_from_token_file(token_path, api_key)
        except FileNotFoundError:
            print('here')
            from selenium import webdriver  # import web crawling library
            with webdriver.Chrome() as driver:
                td = auth.client_from_login_flow(driver, api_key, redirect_uri, token_path)  # if no JSON file exists, redirct to client login

        return(td)

    def pull_options(ticker, date, td):
        import datetime as dt
        import json
        import pandas as pd
        date_time_obj = dt.datetime.strptime(str(date), '%m-%d-%Y')  # convert date to datetime object
        date_delta = (date_time_obj - dt.datetime.now()).days + 1

        read_data = json.load(td.get_option_chain(ticker, contract_type = td.Options.ContractType.PUT,
                                                  from_date = date_time_obj, to_date = date_time_obj)) # call TD's API to get options data and read in the resultant JSON file

        # catch errors ====================================================
        error_encountered = False  # initialize error Boolean
        error_message = None # initialize error msg

        try:
            if read_data['status'] == 'FAILED':
                error_encountered = True
                error_message = 'API error - no puts available on given date'
            else:
                current_price = float(read_data['underlyingPrice'])  # capture current price
                try:
                    data_parsed = read_data['putExpDateMap'][str(dt.datetime.strftime(date_time_obj, '%Y-%m-%d') + ':' + str(date_delta))]  # first data parse
                    error_msg = None
                except:
                    error_msg = 'API error - incorrect expiration date'
                    error_encountered = True

        except:
            error_encountered = True
            error_msg = 'Unexpected API error - no data returned'
        # =============================================================

        puts = pd.DataFrame()  # initialize dataframe to house puts
        if error_encountered is False:
            for a in data_parsed:
                strike_chunk = data_parsed[str(a)][0]  # second data parse

                strings = []  # initialize lists for each data point
                strikes = []
                lasts = []
                volumes = []
                ois = []
                bids = []
                asks = []
                currents = []

                strings.append(str(strike_chunk['symbol']))  # append data to empty lists
                strikes.append(float(strike_chunk['strikePrice']))
                lasts.append(float(strike_chunk['last']))
                volumes.append(float(strike_chunk['totalVolume']))
                ois.append(float(strike_chunk['openInterest']))
                bids.append(float(strike_chunk['bid']))
                asks.append(float(strike_chunk['ask']))
                currents.append(current_price)

                dict = {'String': strings, 'Strike': strikes, 'Last': lasts, 'Volume': volumes, 'Open Interest': ois,
                        'Bid': bids, 'Ask': asks, 'Current': currents}  # merge lists into dictionary

                df = pd.DataFrame(dict)  # merge dictionary into dataframe
                obj = [puts, df]  # merge old and new dataframes to an object
                puts = pd.concat(obj, ignore_index=True)  # re-assign merged object to dataframe

        return(puts, error_message)

    def filter_options(puts, inputs_dict, j):
        import pandas as pd
        pd.set_option('display.max_columns', None) # display max columns

        if puts.empty:
            print(error_msg)
        else:
            print('\nPuts found!')
            puts['Premium'] = round(puts['Last']*100,3) # add Premium column
            puts['VaR'] = round(puts['Strike']*100,3) # add VaR column
            puts['Premium/VaR (%)'] = round(100*puts['Premium']/puts['VaR'],3) # add Premium/VaR column
            puts['Delta (%)'] = round(100*(puts['Current'] - puts['Strike'])/puts['Current'],3) # add Delta column

            if inputs_dict['bid flag'] == True:
                puts = puts[puts['Bid'] > inputs_dict['bid filter']]

            if inputs_dict['premvar flag'] == True:
                puts = puts[puts['Premium/VaR (%)'] > inputs_dict['premvar filter']]

            if inputs_dict['delta flag'] == True:
                puts = puts[puts['Delta (%)'] > inputs_dict['delta filter']]

            if inputs_dict['strike flag'] == True:
                puts = puts[puts['Strike'] > inputs_dict['strike filter']]

            if inputs_dict['volume flag'] == True:
                puts = puts[puts['Volume'] > inputs_dict['volume filter']]

            if puts.empty:
                print(f'\nNo viable {j} puts')
            else:
                print('\nViable puts:')
                print(puts)

        return(puts)