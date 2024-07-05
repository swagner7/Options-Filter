import tkinter as tk
import os
from tkcalendar import Calendar, DateEntry
from OptionsFilter_MainRoutine_v2 import OptionsFilter_MainRoutine_v2
import datetime as dt
import requests
import pandas as pd
from tkinter.filedialog import askopenfilename

#========================================================================================================================================================================
def run_selected():
    if var1.get() == 1:
        bid_flag = 1
    else:
        bid_flag = 0
    if var2.get() == 1:
        prem_flag = 1
    else:
        prem_flag = 0
    if var3.get() == 1:
        delta_flag = 1
    else:
        delta_flag = 0
    if var4.get() == 1:
        strike_flag = 1
    else:
        strike_flag = 0
    if var5.get() == 1:
        volume_flag = 1
    else:
        volume_flag = 0

    date = str(e1.get())
    tickers_list = str(e2.get()).split(',')
    bid_filter = float(e3.get())
    prem_filter = float(e4.get())
    delta_filter = float(e5.get())
    strike_filter = float(e6.get())
    volume_filter = float(e7.get())

    for j in range(len(tickers_list)): # catch lowercase tickers
        tickers_list[j] = tickers_list[j].upper()

    print('OptionsFilter Initiated: ' + str(dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')))
    print(f'Tickers chosen: {tickers_list}')
    print(f'Expiration date chosen: {date}')
    OptionsFilter_MainRoutine_v2(date,tickers_list,bid_flag,prem_flag,delta_flag,strike_flag,volume_flag,bid_filter,prem_filter,delta_filter,strike_filter,volume_filter)
    master.quit()

#============================================================================================================================================================
def run_all():
    if var1.get() == 1:
        bid_flag = 1
    else:
        bid_flag = 0
    if var2.get() == 1:
        prem_flag = 1
    else:
        prem_flag = 0
    if var3.get() == 1:
        delta_flag = 1
    else:
        delta_flag = 0
    if var4.get() == 1:
        strike_flag = 1
    else:
        strike_flag = 0
    if var5.get() == 1:
        volume_flag = 1
    else:
        volume_flag = 0

    date = str(e1.get())
    bid_filter = float(e3.get())
    prem_filter = float(e4.get())
    delta_filter = float(e5.get())
    strike_filter = float(e6.get())
    volume_filter = float(e7.get())
    if len(date) == 0:
        raise(NameError('No date enetered'))

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

    r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params)
    data = r.json()['data']
    tickers_list = pd.DataFrame(data['rows'], columns=data['headers'])

    tickers_list = list(tickers_list['symbol'])

    tickers_list = [item for item in tickers_list if item.find('^') == -1] # filter out tickers with '^'
    tickers_list = [item for item in tickers_list if item.find('/') == -1] # filter out tickers with '/'

    OptionsFilter_MainRoutine_v2(date,tickers_list,bid_flag,prem_flag,delta_flag,strike_flag,volume_flag,bid_filter,prem_filter,delta_filter,strike_filter,volume_filter)
    master.quit()

#========================================================================================================================================================================
def run_calendar():
    def confirm_sel():
        cal_date = cal.get_date()
        e1.delete(0,'end')
        e1.insert(0,str(cal_date))
        top.destroy()

    top = tk.Toplevel(master)

    cal = Calendar(top, selectmode='day', date_pattern='mm-dd-yyyy')
    cal.pack(fill="both", expand=True)
    tk.Button(top, text="Select", command=confirm_sel).pack()

#startGUI================================================================================================================================================================
master = tk.Tk()
master.title('Options Filter GUI')

# labels
tk.Label(master,text='Required:').grid(row=0)
tk.Label(master,text='Expiration Date (mm-dd-yyyy)').grid(row=1)
tk.Label(master,text='Optional:').grid(row=3)
tk.Label(master,text='Tickers (separate with comma)').grid(row=4)
tk.Label(master,text='').grid(row=5)
tk.Label(master,text='%').grid(row=2,column=4)
tk.Label(master,text='%').grid(row=3,column=4)

# dialog boxes
e1 = tk.Entry(master)
e1.grid(row=1, column=1) # expiration date
e2 = tk.Entry(master)
e2.grid(row=4, column=1) # tickers list
e3 = tk.Entry(master)
e3.grid(row=1, column=3) # bid filter
e3.insert(0,1)
e4 = tk.Entry(master)
e4.grid(row=2, column=3) # prem filter
e4.insert(0,1)
e5 = tk.Entry(master)
e5.grid(row=3, column=3) # delta filter
e5.insert(0,10)
e6 = tk.Entry(master)
e6.grid(row=4, column=3) # strike filter
e6.insert(0,10)
e7 = tk.Entry(master)
e7.grid(row=5, column=3) # volume filter
e7.insert(0,5)


# buttons
tk.Button(master,text='Open Calendar',command=run_calendar).grid(row=2,column=1)
tk.Button(master,text='Run All Tickers',command=run_all).grid(row=7,column=0)
tk.Button(master,text='Run Selected Tickers',command=run_selected).grid(row=7,column=1)
tk.Button(master,text='Quit',command=master.quit).grid(row=7,column=3)

# check boxes
tk.Label(master,text='Choose filters:').grid(row=0,column=2)
var1 = tk.IntVar()
var1.set(1)
tk.Checkbutton(master, text="Bid > ", variable=var1, onvalue = 1, offvalue = 0).grid(row=1,column=2)
var2 = tk.IntVar()
var2.set(1)
tk.Checkbutton(master, text="Premium/VAR >", variable=var2, onvalue = 1, offvalue = 0).grid(row=2,column=2)
var3 = tk.IntVar()
var3.set(1)
tk.Checkbutton(master, text="Delta >", variable=var3, onvalue = 1, offvalue = 0).grid(row=3,column=2)
var4 = tk.IntVar()
var4.set(1)
tk.Checkbutton(master, text="Strike >", variable=var4, onvalue = 1, offvalue = 0).grid(row=4,column=2)
var5 = tk.IntVar()
var5.set(1)
tk.Checkbutton(master, text="Volume >", variable=var5, onvalue = 1, offvalue = 0).grid(row=5,column=2)

tk.mainloop()
