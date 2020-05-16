from get_cdata import get_coins_data
from etl import get_names
import json
from get_cdata import get_coin_data
from get_idata import get_trend_data

"""This module can be used to add more data to .csv file store"""


jfile=open("config.json")
config=json.load(jfile)
jfile.close()

BASE_PATH=config["data"]["base_path"]
CSAVE_PATH=os.path.join(BASE_PATH,"coins/")
ISAVE_PATH=os.path.join(BASE_PATH,"interest/")

now=datetime.datetime.now()

##get yesterdat at 1 AM
end_date=

for filename in os.listdir(CSAVE_PATH):
    
    #get ticker
    df=pd.read_csv(os.path.join(BASE_PATH,"coins.csv"))
    
    name=filename.replace(".csv","")
    symbol=df[df.name==name].symbol.values[0].upper()
    PAIR=symbol+BASE_COIN
    
    #get data
    data=get_coin_data(name=name,pair=PAIR,end_date=end_date)

sleep_time=0
for filename in os.listdir(ISAVE_PATH):
    get_idata(kw=name,end_date=end_date)
    sleep_time=sleep_time+72
    time.sleep(sleep_time)
            