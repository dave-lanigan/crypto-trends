import psycopg2
from psycopg2 import sql
import json
from etl import get_names_set
"""This script can be used to test the config.json file to check database connection and data path."""


json_file=open("config.json")
config = json.load(json_file)


conn=psycopg2.connect(
"host={} dbname={} user={}".format( config["postgres"]["host"],
                                    config["postgres"]["db_name"],
                                    config["postgres"]["db_user"] ))

cur = conn.cursor()

# table_names=get_names_set()
# sum=0
# for table in table_names:
#     q=sql.SQL("SELECT count(*) FROM _{}_").format( sql.SQL(table) )
    
#     cur.execute( q )
#     sum=sum+int( cur.fetchone()[0] )
# print("total rows:", sum)
# conn.close()

print("connection works!")
print("The data path is: {}".format(config["data"]["base_path"]))
