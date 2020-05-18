import os
import json
from psycopg2 import sql
import psycopg2
from datetime import datetime
import pandas as pd
from etl import get_names_set


jfile=open("config.json")
config=json.load(jfile)
jfile.close()
BASE_PATH=config["data"]["base_path"]
SQL_FLAG=config["data"]["sql_flag"]
conn=psycopg2.connect(
"host={} dbname={} user={}".format( config["postgres"]["host"],
                                    config["postgres"]["db_name"],
                                    config["postgres"]["db_user"] ))

cur = conn.cursor()

table_names=get_names_set(BASE_PATH,form="sql")
coin_names=get_names_set(BASE_PATH,form="basic")

len_fails,date_fails=[],[]
for i,table in enumerate(table_names):
    name=coin_names[i]
    print("checking table for {}".format(name))
    coindf=pd.read_csv(os.path.join(BASE_PATH,"coins/{}.csv".format(name)))
    start_date=coindf[0:1]
    start_date=start_date.values[0][0]
    
    cur.execute(sql.SQL("SELECT * FROM _{}_ LIMIT 1;").format( sql.SQL(table) ) )

    out=cur.fetchone()
    sql_date=out[0]

    if len(out)==10:
        print("Row length test PASSED.")
    elif len(out) != 10:
        print("Row length test FAILED.")
        len_fails.append(name)
        
    if sql_date==start_date:
        print("Row length test PASSED.")
    elif sql_date!=start_date:
        print("Row length test FAILED.")
        date_fails.append(name)

print(" ")
print(" ")
print("Tests complete.")
print(" ")
print("Table Row Length Test Fails; Number: {}".format(len(len_fails)))
print("Table Row Length Test Fails; Coins: {}".format( " ".join(len_fails) ) ) 
print(" ")
print("Table Date Test Fails; Number: {}".format(len(date_fails)))
print("Table Date Test Fails; Coins: {}".format( " ".join(date_fails) ) )
