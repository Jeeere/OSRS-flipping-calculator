import requests
import sqlite3
import json

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

def reset_mapping():
    """
    Gets new mapping information and replaces old
    """
    response = requests.get("https://prices.runescape.wiki/api/v1/osrs/mapping",headers=headers).json()
    for item in response:
        c.execute("INSERT INTO mapping VALUES (:id, :examine, :members, :lowAlch, :buyLimit, :value, :highAlch, :icon, :name)", {
                    'id': item["id"],
                    'examine': item["examine"],
                    'members': item["members"],
                    'lowAlch': item["lowalch"],
                    'buyLimit': item["limit"],
                    'value': item["value"],
                    'highAlch': item["highalch"],
                    'icon': item["icon"],
                    'name': item["name"]
                    })
        conn.commit()

def get_data(headers):
    """
    Saves API response to test.json
    """
    response = requests.get("https://prices.runescape.wiki/api/v1/osrs/5m",headers=headers).json()
    with open('test.json', 'w') as f:
        json.dump(response, f)

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

def main(headers):
    get_data(headers)

if __name__ == "__main__":
    main(headers)