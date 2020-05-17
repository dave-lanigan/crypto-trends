##outside
import json
from binance import client
from binance.client import Client
from binance.websockets import BinanceSocketManager
import dateparser
import os
from datetime import datetime
import requests
import pandas as pd
from pytrends.request import TrendReq
import time


"""
This module has function to retrieve coin info, price, and google trends data and save to .csv files
"""

def get_coin_names_all(base_path,form="tickers"):
    """Returns both tickers and names"""
    cpath=os.path.join(base_path,"coins")
    cnames=[]
    for filename in os.listdir(cpath):
        idx=filename.find(".")
        cnames.append(filename[:idx])

    df=pd.read_csv( os.path.join(base_path,"coins.csv") )
    df=df[ (df.name).isin(cnames) ]
    
    names,symbols=df["name"].values,df["symbol"].values
    if form=="tickers":
        return symbols
    if form=="names":
        return names

def convert_date(date):
    """Converts ISO 8601 date to a human readable format
    Arguments:
        date {str}: Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
    Returns:
        ndate {str}: a human readable date
    """
    time=datetime.strptime(date, "%Y-%m-%dT%H")
    hour=time.hour
    if hour<12:
        ampm="AM"
        if hour==0:
            hour = "12"
    elif hour>=12:
        ampm="PM"
        if hour>12:
            hour = int(hour)-12

    return "{} {}, {} {}:00 {} EST".format( time.strftime("%B"), time.day, time.year, hour, ampm )

def get_info():
    """Collects and saves to .csv a list of the top 50 coins from coingeck api."""
    
    print("Getting coin info data...")
    base_url="https://api.coingecko.com/api/v3/coins/"
    out=requests.get(base_url)
    coins=out.json()


    coin_list=[]
    for c in coins:
        coin_list.append(c["id"])
        
    coins=[["coingecko_id","symbol","name","market_cap_rank","links","description"]]
    for coin in coin_list:
        nurl=base_url+coin
        out=requests.get(nurl)
        coin=out.json()
        aL=[coin["id"],coin["symbol"],coin["name"],coin["market_cap_rank"]]
        try:
            aL.append( coin["links"]["homepage"][0] )
        except:
            aL.append("NULL")
        try:
            aL.append( coin["description"]["en"] )
        except:
            aL.append("NULL")
            
        coins.append(aL)
        

    df=pd.DataFrame(data=coins[1:],columns=coins[0])
    df.to_csv("../data/coins.csv",index=False)
    
    print("Data saved.")

def get_coin_data(get_flag="",path="",name="",pair="",start_date="", end_date="",convert_date=convert_date):
    
    """Collects coin price data from binance API saves a .csv file.
    Arguments:
        get_flag {str}: If left blank the function defaults to the whats in the config file.
        path {str}: where .csv will be saved. The function defaults to to the path data/coins/ if path is blank.
        pair {str}: cryptocurrency pair like: "BTCUSDT" = Bitcoin and Tether.
        start_date {str}: Date in the ISO 8601 format *with hour* YYYY-MM-DDT01 - Can be left blank the default is "2015-05-01T00" for collect.
        end_date {str}:Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        
    Returns:
        Nothing.
    """
    ##set up
    jfile=open("config.json")
    config=json.load(jfile)

    fname="{}.csv".format( name.replace(" ","-"))
        
    if path=="":
        path=os.path.join(config["data"]["base_path"],"coins/")
    if get_flag=="":
        get_flag=config["data"]["coins_get"]
    jfile.close()
   
    if get_flag=="collect":
        status="w+"
        if start_date=="":
            start_date=="May 1, 2015 12:00 AM EST"
    elif get_flag=="append":
        write_status="a+"

        ###get start date from file
        if start_date != "":
            print("Warning the start_date should be left blank for appending so that the last end_date is used.")
            
            if datetime.strptime(start_date, "%Y-%m-%dT%H") >= datetime.strptime(end_date, "%Y-%m-%dT%H"):
                print("Data acquisition already satisfied")
                return False
        
        elif start_date=="":
            coin_path=os.path.join(config["data"]["base_path"],"coins/{}".format(fname))
            coindf=pd.read_csv( coin_path )
            start_date=coindf["open_time_iso"].iloc[-1:].values[0][:-6].replace(" ","T")
            print(start_date)
            if datetime.strptime(start_date, "%Y-%m-%dT%H") >= datetime.strptime(end_date, "%Y-%m-%dT%H"):
                print("Data acquisition already satisfied")
                return False

    print("Getting data for Coin: {}, Pair: {}, dates: {} to {}".format(name,pair,start_date,end_date))
    start_date,end_date=convert_date(start_date),convert_date(end_date)
    print(start_date,end_date)
    
    client=Client()
    klines= client.get_historical_klines(pair,
                                         Client.KLINE_INTERVAL_1HOUR,
                                         start_date,
                                         end_date)
    

    save_path=os.path.join(path,fname)

    print("Got data. Now {}ing...".format(get_flag))
    with open(save_path,write_status) as f:
        if write_status=="collect":
            f.write("open_time_iso,open_time_unix,open,high,low,close,volume,close_time,number_of_trades\n")
        for kline in klines:
            f.write( "{},{},{},{},{},{},{},{},{}\n".format(
            datetime.fromtimestamp(kline[0]/1000).isoformat().replace("T"," "),
                                                    kline[0],
                                                    kline[1],
                                                    kline[2],
                                                    kline[3],
                                                    kline[4],
                                                    kline[5],
                                                    kline[6],
                                                    kline[8]
                                                    ) )

    print("Data saved here {}.".format(save_path))
    
def get_trend_data(get_flag="",path="",kw="",start_date="",end_date=""):
    
    """Collects google trends data based on keyword and saves a .csv file.
    Arguments:
        get_flag {str}: Flag either "append" or "collect" - si defined in the config file
        kw {str}: Search term.
        path {str}: where .csv will be saved. The function defaults to the path data/interests/ if path is blank
        start_date {str}: Date in the ISO 8601 format *with hour* YYYY-MM-DDT01. *Should almost ALWAYS be left blank*
        end_date {str}:Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        
    Returns:
        Nothing.
    Pre-set parameters: geo="",timezone=eastern
    """
    ##set up
    pytrend = TrendReq( hl="en-US" , tz=300)
    jfile=open("config.json")
    config=json.load(jfile)

    fname="{}.csv".format( kw.replace(" ","-") )
    interest_path=os.path.join(config["data"]["base_path"],"interest/{}".format(fname))
    coin_path=os.path.join(config["data"]["base_path"],"coins/{}".format(fname))
        
    if path=="":
        path=os.path.join(config["data"]["base_path"],"interest/")
    if get_flag=="":
        get_flag=config["data"]["trends_get"]
    jfile.close()
    
    if get_flag=="collect":
        if start_date=="":
            coindf=pd.read_csv( coin_path )
            start_date=coindf["open_time_iso"].iloc[-1:].values[0][:-6].replace(" ","T")
        elif start_date != "":
            print("Warning. You posted a start date. General you want to leave this blank so that the price data start date automatically is used.")

    elif get_flag=="append":
        if start_date != "":
            print("Warning. You posted a start date. General you want to leave this blank so that the last date automatically used.")
            if datetime.strptime(start_date, "%Y-%m-%dT%H") >= datetime.strptime(end_date, "%Y-%m-%dT%H"):
                print("Data acquisition already satisfied")
                return False

        elif start_date=="":
            intdf=pd.read_csv( interest_path )
            start_date=intdf["date"].iloc[-1:].values[0][:-6].replace(" ","T")
            if datetime.strptime(start_date, "%Y-%m-%dT%H") >= datetime.strptime(end_date, "%Y-%m-%dT%H"):
                print("Data acquisition already satisfied")
                return False


    dt1 = datetime.strptime(start_date, '%Y-%m-%dT%H')
    dt2 = datetime.strptime(end_date, '%Y-%m-%dT%H')
    
    print("Getting interest data for Coin: {}, dates: {} to {}".format(kw,start_date,end_date))    
    df=pytrend.get_historical_interest([kw],
                                    year_start=dt1.year,
                                    month_start=dt1.month, 
                                    day_start=dt1.day, 
                                    hour_start=dt1.hour, 
                                    year_end=dt2.year, 
                                    month_end=dt2.month,
                                    day_end=dt2.day, 
                                    hour_end=dt2.hour, 
                                    cat=0, 
                                    geo='', 
                                    gprop='', 
                                    sleep=120
                                    )

    
    save_path=interest_path

    if get_flag=="collect":
        df.to_csv(save_path)
    elif get_flag=="append":  
        with open(save_path,"a+") as f:
            for row in df.values:
                f.write("{},{},{}".format(row[0],row[1],row[2]))
            f.close()
    
    print("file {}ed here {}.".format(get_flag,save_path))

if __name__ == "__main__":
    
    jfile=open("config.json")
    config=json.load(jfile)
    jfile.close()

    BASE_PATH=config["data"]["base_path"]
    CSAVE_PATH=os.path.join(BASE_PATH,"coins/")
    GET_FLAG=config["data"]["coins_get"]
    BASE_COIN="USDT"


    #get_coin_data(get_flag="collect",name="Nano",pair="NANOUSDT",start_date=start_date,end_date=end_date) 
    #get_trend_data(kw="",end_date="")
