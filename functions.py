import json
import requests

def get_flip_profit(settings):
    """
    Function to calculate flip profits for all items
    """
    profits = {}

    with open('test.json', 'r') as f:       # Load json containing trading information
        data = json.load(f)
    with open('limits.json', 'r') as m:     # Load json containing buy limits
            limits = json.load(m)
    for key in data:                        # Loop through every item in data
        try:                                # Try for high and low prices, continue if not found
            margin = data[key]["avgHighPrice"] - data[key]["avgLowPrice"]
        except:
            continue
        limit = limits[key]                 # Find buy limit for item
        if limit:
            profit = limit * margin         # Calculate profit if buy limit exists
        else:
            profit = None                   # Set profit to None if there is no buy limit for item
        try:                                # Try for missing volume information
            if profit and profit >= settings.flip_profit_threshold and data[key]["highPriceVolume"] >= settings.flip_highVolume_threshold and data[key]["lowPriceVolume"] >= settings.flip_lowVolume_threshold:
                profits[key] = {}           # Create new dictionary for item and update it with flip information
                profits[key].update({"prices": [data[key]["avgHighPrice"], data[key]["avgLowPrice"]], "limit":limit, "margin":margin, "profit":profit, "roi": get_roi(data[key]["avgHighPrice"], data[key]["avgLowPrice"])})
        except KeyError:
            continue

    return profits

def reset_mapping(headers):
    """
    Gets new mapping information and replaces old
    """
    response = requests.get("https://prices.runescape.wiki/api/v1/osrs/mapping",headers=headers).json()
    with open('mapping.json', 'w') as f:    # Replace old mapping file with new
        json.dump(response, f)

    # for item in response:
    #     c.execute("INSERT INTO mapping VALUES (:id, :examine, :members, :lowAlch, :buyLimit, :value, :highAlch, :icon, :name)", {
    #                 'id': item["id"],
    #                 'examine': item["examine"],
    #                 'members': item["members"],
    #                 'lowAlch': item["lowalch"],
    #                 'buyLimit': item["limit"],
    #                 'value': item["value"],
    #                 'highAlch': item["highalch"],
    #                 'icon': item["icon"],
    #                 'name': item["name"]
    #                 })
    #     conn.commit()
    get_limits()                            # Run get_limits() to get new buy limits file
    return

def get_limits():
    """
    Fetch buy limits from mapping file and dump to limits file
    """
    limits = {}
    with open('mapping.json', 'r') as m:
        mapping = json.load(m)
    for d in mapping:                       # Loop through dictionaries in mapping file
        try:
            limits[d["id"]] = d["limit"]    # Fetch limit from dictionary
        except KeyError:
            limits[d["id"]] = None          # Set limit to None if limit doesnt exist

    with open('limits.json', "w") as l:     # Dump limits to json
        json.dump(limits,l)
    return

def get_metadata(ids, examine=False, members=False, lowalch=False, limit=False, value=False, highalch=False, icon=False, name=False):
    """
    Get requested data for item ID
    ids: list of ids to search
    """
    data = {}
    with open('mapping.json', 'r') as m:
        mapping = json.load(m)
    while ids:
        result = [item for item in mapping if item["id"] in ids][0] # Search mapping for id in ids
        ids.remove(result["id"])                                    # Remove id from ids
        data[result["id"]] = {}                                     # Create result dictionary for id
        # Update result dictionary with wanted information
        if examine == True:
            data[result["id"]]["examine"] = result["examine"]
        if  members == True:
            data[result["id"]]["members"] = result["members"]
        if  lowalch == True:
            data[result["id"]]["lowalch"] = result["lowalch"]
        if  limit == True:
            try:    # If no buy limit replace with None
                data[result["id"]]["limit"] = result["limit"]
            except KeyError:
                data[result["id"]]["limit"] = None
        if  value == True:
            data[result["id"]]["value"] = result["value"]
        if  highalch == True:
            data[result["id"]]["highalch"] = result["highalch"]
        if  icon == True:
            data[result["id"]]["icon"] = result["icon"]
        if  name == True:
            data[result["id"]]["name"] = result["name"]
    
    return data

def get_min_limit(ids):
    """
    Fetches limits for list of ids and returns smallest.
    """
    data = get_metadata(ids, limit=True)    # Get dictionary of buy limits for list of ids
    limit_dicts = list(data.values())       # Trasnform into list of limit dictionaries
    limits = []
    for dict in limit_dicts:                # Loop through dictionaries
        limits.append(dict["limit"])        # Append limit to limits
    if None in limits:                      # If items had no buy limits return None
        return None
    else:                                   # Else return minimum value in list
        return min(limits)

def get_roi(high, low):
    """
    Function to calculate return of investment
        high: sell price
        low: buy price
    """
    try:
        roi = round((high / low) * 100,1)
        return roi
    except TypeError:
        return None

def get_prices(prices, all=False):
    """
    Replaces dictionary of ids with dictionary of prices.
        prices: {[highPrice, lowPrice, lowPrice, ...],[...],[...]}
        all:    True: Fetches high and low prices for all ids
                False: Fetches high price for first id, low price for rest
    """
    with open('test.json', 'r') as f:   # Load trading information file
            data = json.load(f)

    for key, ids in prices.items():     # Iterate through given dict
        lst = []                        # New list to replace one in dictionary
        for n in ids:                   # Iterate through list in dict
            try:
                if all:
                    lst.append((data[str(n)]["avgHighPrice"], data[str(n)]["avgLowPrice"]))
                elif not all and n == ids[0]:         # If first element in list get high price
                    lst.append((data[str(n)]["avgHighPrice"]))
                elif not all:                   # Else get low price
                    lst.append((data[str(n)]["avgLowPrice"]))
            except KeyError:            # If inactive append None
                if not all:
                    lst.append(None)
                elif all:
                    lst.append((None, None))
        prices[key] = lst               # Update returning dict with fetched information

    return prices