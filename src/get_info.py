import requests
import pandas as pd



def get_info():

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


get_info()
