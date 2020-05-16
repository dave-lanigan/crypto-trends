import psycopg2
from psycopg2 import sql
import json

"""This script can be used to test the config.json file to check database connection and data path."""


json_file=open("config.json")
config = json.load(json_file)


conn=psycopg2.connect(
"host={} dbname={} user={}".format( config["postgres"]["host"],
                                    config["postgres"]["db_name"],
                                    config["postgres"]["db_user"] ))

cur = conn.cursor()

print("connection works!")
print("The data path is: {}".format(config["data"]["base_path"]))
