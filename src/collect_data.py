import json
from get_data import get_coin_data, get_trend_data, get_info

"""This module can be used to collect all the data for the first time"""

jfile=open("config.json")
config=json.load(jfile)
jfile.close()

BASE_COIN_TICKER,BASE_COIN_NAME=config["base_coin"]["ticker"],config["base_coin"]["name"]
BASE_PATH=config["data"]["base_path"]
df=pd.read_csv( os.path.join(BASE_PATH,"coins.csv") )
names,symbols=df["name"].values,df["symbol"].values

##get coin info
get_info()

##get price data
failed=[]
for i,name in enumerate(names):
    if name != BASE_COIN_NAME:

        PAIR=str(symbols[i].upper())+BASE_COIN_TICKER

        try:
            print("Trying {}".format(PAIR))
            get_coin_data(name=name,pair=PAIR,end_date="2020-05-01T00")
        except:
            print("Saving coin data for {} failed".format(name))
            failed.append((name,"coin data" ))

with open( os.path.join(BASE_PATH,"failed.csv"),"w+") as f:
    f.write( ",",join(failed) )

##get interest data
sleep_time=720
for filename in os.listdir(CDATA_PATH):
    df=pd.read_csv( os.path.join( CDATA_PATH,filename) )
    name=filename[:filename.find(".")].replace("-"," ")

    get_idata(get_flag="collect",kw=name,end_date="2020-05-01T00")
    sleep_time=sleep_time+72
    time.sleep(sleep_time)
            
            
    
    
