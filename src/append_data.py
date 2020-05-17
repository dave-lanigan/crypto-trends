import json
from get_data import get_coin_data, get_trend_data
import os
import pandas as pd
import time
"""This module can be used to add more data to .csv file store"""


jfile=open("config.json")
config=json.load(jfile)
jfile.close()

BASE_PATH=config["data"]["base_path"]
CSAVE_PATH=os.path.join(BASE_PATH,"coins/")
ISAVE_PATH=os.path.join(BASE_PATH,"interest/")
BASE_COIN=config["base_coin"]["ticker"]

end_date="2020-05-02T00"

for filename in os.listdir(CSAVE_PATH):
    if ".csv" in filename:
        #get ticker
        df=pd.read_csv(os.path.join(BASE_PATH,"coins.csv"))
        name=filename.replace(".csv","").replace("-"," ")
        print(name)
        symbol=df[df.name==name].symbol.values[0].upper()
        PAIR=symbol+BASE_COIN
        
            #get data
        data=get_coin_data(name=name,pair=PAIR,end_date=end_date)

sleep_time=0
for filename in os.listdir(ISAVE_PATH):
    if ".csv" in filename:
        name=filename.replace(".csv","").replace("-"," ")
        get_trend_data(kw=name,end_date=end_date)
        sleep_time=sleep_time+72
        time.sleep(sleep_time)
                