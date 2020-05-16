##outside
import json
from binance import client
from binance.client import Client
from binance.websockets import BinanceSocketManager
import dateparser
import os
from datetime import datetime
import pandas as pd

"""

"""


def get_coin_data(get_flag,path="",name="",pair="",start_date="", end_date=""):
    
    """Collects coin price data from binance API saves a .csv file.
    Arguments:
        path {str}: where .csv will be saved.
        pair {str}: cryptocurrency pair like: "BTCUSDT" = Bitcoin and Tether 
        start_date {str}: Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        end_date {str}:Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        
    Returns:
        Nothing.
    """
    print("Getting data for Coin: {}, Pair: {}, Up to Date: {}".format(name,pair,end_date))
    client=Client()
    klines= client.get_historical_klines(pair,
                                         Client.KLINE_INTERVAL_1HOUR,
                                         start_date,
                                         end_date)
    
    #klines=klines[::-1]
    print("Got data. Now saving...")
    d1,d2=dateparser.parse(start_date),dateparser.parse(end_date)
    
    fname="{}.csv".format( name )
    save_path=os.path.join(path,fname)
    
    if get_flag=="collect":
        status="w+"
    elif get_flag=="append":
        status="a+"


    with open(save_path,status) as f:
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

    print("Data saved here: {}".format(save_path))
    
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
    """
    Arguments:
        date {str}: the date as a string as iso
    Returns:
        ndate {str}: a human readable date
    """
    time=datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    ######-----

    return "{} {}, {} 12:00 AM EST".format( time.strftime("%b"), time.day, time.year)

def get_coins_data(GET_FLAG,BASE_PATH, start_date="", end_date=""):
    
    now=datetime.datetime.now()
    
    CSAVE_PATH=os.path.join(BASE_PATH,"coins")

    if GET_FLAG=="collect":
        start_date,end_date='May 1, 2015 12:00 AM EST','May 1, 2020 12:00 AM EST'

        df=pd.read_csv( os.path.join(BASE_PATH,"coins.csv") )

        names,symbols=df["name"].values,df["symbol"].values

        failed=[]
        for i,name in enumerate(names):
            if name != "Tether":
            
                PAIR=str(symbols[i].upper())+BASE_COIN
                
                try:
                    print("Trying {}".format(PAIR))
                    get_coin_data(path=CSAVE_PATH,name=name,pair=PAIR,start_date=start_date,end_date=end_date)
                except:
                    print("Saving coin data for {} failed".format(name))
                    failed.append((name,"coin data" ))

        with open( os.path.join(BASE_PATH,"failed.csv"),"w+") as f:
            f.write( ",",join(failed) )

    if GET_FLAG=="append":
        now=datetime.datetime.now()
        if end_date=="":
            end_date="{} {}, {} 12:00 AM EST".format( now.strftime("%b"), now.day, now.year)
        for filename in os.listdir(CSAVE_PATH):
            #get date
            coindf=pd.read_csv( os.path.join(CSAVE_PATH,filename) )
            date=coindf.head().values[0][0]
            
            ##########-
            start_date=convert_date(date)
            
            #get ticker
            df=pd.read_csv(os.path.join(BASE_PATH,"coins.csv"))
            
            name=filename.replace(".csv","")
            symbol=df[df.name==name].symbol.values[0].upper()
            PAIR=symbol+BASE_COIN
            
            #get data
            data=get_coin_data(get_flag, path=CSAVE_PATH,name=name,pair=PAIR,start_date=start_date,end_date=end_date)
            


if __name__ == "__main__":
    
    
    jfile=open("config.json")
    config=json.load(jfile)
    jfile.close()

    BASE_PATH=config["data"]["base_path"]
    CSAVE_PATH=os.path.join(BASE_PATH,"coins/")
    GET_FLAG=config["data"]["coins_get"]
    BASE_COIN="USDT"

    start_date,end_date='May 1, 2015 12:00 AM EST','May 1, 2020 12:00 AM EST'
    get_coin_data(get_flag="collect", path=CSAVE_PATH,name="Nano",pair="NANOUSDT",start_date=start_date,end_date=end_date)
    
    #get_coins_data()
