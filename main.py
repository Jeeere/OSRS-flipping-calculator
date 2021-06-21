from json.decoder import JSONDecodeError
import requests
import sqlite3
import json
import timeit

from recipes import *
from settings import *
import functions as fn

headers = {"User-Agent": "Profit analyzer (early development) / Jeere#8533"} # set user agent for request
conn = sqlite3.connect('database.db') # set connection for sqlite
c = conn.cursor() # set cursor


def initialize_tables():
    """
    Creates database tables
    """
    c.execute("""CREATE TABLE IF NOT EXISTS mapping (
                id integer PRIMARY KEY,
                examine text DEFAULT "",
                members boolean DEFAULT 0,
                lowAlch integer,
                buyLimit integer,
                value integer,
                highAlch integer,
                icon text DEFAULT "",
                name text DEFAULT ""
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS prices5m (
                id integer PRIMARY KEY,
                avgHighPrice integer,
                highPriceVolume integer,
                avgLowPrice integer,
                lowPriceVolume integer,
                timestamp integer
                )""")

def get_data(headers):
    """
    Saves API response to test.json
    """
    response = requests.get("https://prices.runescape.wiki/api/v1/osrs/5m",headers=headers).json()
    response = response["data"]

    with open('test.json', 'r') as f:
        try:
            data = json.load(f)
        except JSONDecodeError: # Fail and return raw response if file empty
            return response
        for key1, dict in response.items():     # Iterate through item IDs in response
            for key2, value in dict.items():    # Iterate through items
                if value:                       
                    try:
                        data[key1][key2] = value    # Replace value in file with one in response if exists
                    except KeyError:                # Create new key-value pair if doesn't exist
                        data[key1] = {}
                        data[key1][key2] = value
    return data

def dump_data(data):
    """
    Dumps data to json
    """
    with open('test.json', 'w') as f:
        json.dump(data, f)

def data2db():
    """
    Moves data from .json to database
    """
    with open('test.json', 'r') as f:
        data = json.load(f)
        items = data["data"]
        for itemId in items:
            item = items[itemId]
            print(itemId, item["avgHighPrice"], item["highPriceVolume"], item["avgLowPrice"], item["lowPriceVolume"])
            c.execute("INSERT INTO prices5m VALUES (:id, :HiPrice, :HiVol, :LoPrice, :LoVol, :time)", {
                      'id': itemId,
                      'HiPrice': item["avgHighPrice"],
                      'HiVol': item["highPriceVolume"],
                      'LoPrice': item["avgLowPrice"],
                      'LoVol': item["lowPriceVolume"],
                      'time': data["timestamp"]
                      })
            conn.commit()
            pass

    #c.execute("SELECT * FROM prices5m WHERE id=:id", {'id':2})
    c.execute("SELECT * FROM mapping")
    print(c.fetchall())

    conn.commit()   # commit changes to db
    conn.close()    # close db

#########################################
def main(headers):
    """
    Main function
    """
    settings = Settings()
    #fn.reset_mapping(headers)
    dump_data(get_data(headers))
    decant = Decant(settings)
    combine = Combine(settings)
    pay = Pay(settings)
    print  ('##################################################')
    print  ("##############      UNF PROFIT      ##############\n" + str(pay.unfinished_potions_profit()))
    print  ("##############     CRUSH PROFIT     ##############\n" + str(pay.crush_profit()))
    print  ("############## 3 TO 4 DECANT PROFIT ##############\n" + str(decant.three_to_four()))
    print  ("##############  MAX DECANT PROFIT   ##############\n" + str(decant.max_profit()))
    print  ("##############  MAX COMBINE PROFIT  ##############\n" + str(combine.combine_profit()))
    print  ("##############     FLIP PROFIT      ##############\n" + str(fn.get_flip_profit(settings)))

#########################################
if __name__ == "__main__":
    start = timeit.default_timer()
    main(headers)
    print('##################################################\nTime: ', timeit.default_timer() - start)  