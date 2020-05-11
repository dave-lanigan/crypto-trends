import configparser
from binance import client
from binance.client import Client
from binance.websockets import BinanceSocketManager
import dateparser
import os
from datetime import datetime


def get_cdata(path="",name="",pair="",start_date="", end_date=""):
    
    """Collects coin price data from binance API saves a .csv file.
    Arguments:
        path {str}: where .csv will be saved.
        pair {str}: cryptocurrency pair like: "BTCUSDT" = Bitcoin and Tether 
        start_date {str}: Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        end_date {str}:Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        
    Returns:
        Nothing.
    """
    print("Getting data...")
    client=Client()
    klines= client.get_historical_klines(pair,
                                         Client.KLINE_INTERVAL_1HOUR,
                                         start_date,
                                         end_date)
    
    print(klines[10])
    
    #klines=klines[::-1]
    print("Got data. Now saving...")
    d1,d2=dateparser.parse(start_date),dateparser.parse(end_date)
    
    fname="{}.csv".format( name )
    save_path=os.path.join(path,fname)
    
    with open(save_path,"w+") as f:
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
    
if __name__ == "__main__":
    
    import pandas as pd
    
    CSAVE_PATH="../data/coins"

    start_date,end_date='May 1, 2015 12:00 AM EST','May 1, 2020 12:00 AM EST'
    BASE_COIN="USDT"
    
    
    df=pd.read_csv("../data/coins.csv")
    
    names,symbols=df["name"].values,df["symbol"].values
    
    failed=[]
    for i,name in enumerate(names):
        if name != "Tether":
        
            PAIR=str(symbols[i].upper())+BASE_COIN
            
            try:
                print("Trying {}".format(PAIR))
                get_cdata(path=CSAVE_PATH,name=name,pair=PAIR,start_date=start_date,end_date=end_date)
            except:
                print("Saving coin data for {} failed".format(name))
                failed.append((name,"coin data" ))

    with open("data/failed.csv","w+") as f:
        f.write( ",",join(failed) )

     
