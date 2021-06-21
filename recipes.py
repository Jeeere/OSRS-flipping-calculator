import json
import functions as fn

class Decant():
    """
    Calculates profit for decanting potions
    """
    def __init__(self, settings):
        self.settings = settings

        self.potions = {#"Potion":  [1dose,2dose,3dose,4dose],
                    "Agility":      [3038,3036,3034,3032],
                    "Antifire":     [2458,2456,2454,2452],
                    "Attack":       [125,123,121,2428],
                    "Bastion":      [22470,22467,22464,22461],
                    "Battlemage":   [22458,22455,22452,22449],
                    "Combat":       [9745,9743,9741,9739],
                    #"Compost":      [6476,6474,6472,6470],
                    "Defence":      [137,135,133,2432],
                    "Divine bastion":     [24644,24641,24638,24635],
                    "Divine battlemage":  [24632,24629,24626,24623],
                    "Divine magic":       [23754,23751,23748,23745],
                    "Divine ranging":     [23742,23739,23736,23733],
                    "Divine super attack":     [23706,23703,23700,23697],
                    "Divine super combat":     [23694,23691,23688,23685],
                    "Divine super defence":    [23730,23727,23724,23721],
                    "Divine super strength":   [23718,23715,23712,23709],
                    "Energy":       [3014,3012,3010,3008],
                    "Fishing":      [155,153,151,2438],
                    "Hunter":       [10004,10002,10000,9998],
                    "Magic":        [3046,3044,3042,3040],
                    "Prayer":       [143,141,139,2434],
                    "Ranging":      [173,171,169,2444],
                    "Restore":      [131,129,127,2430],
                    "Stamina":      [12631,12629,12627,12625],
                    "Strength":     [119,117,115,113],
                    "Super antifire":    [21987,21984,21981,21978],
                    "Super combat":      [12701,12699,12697,12695]}
        
        self.prices = fn.get_prices(self.potions.copy(), all=True)

    # def get_prices(self):
    #     """
    #     Get prices for all tradeable potions
    #     ids: list of ids to fetch prices for
    #     """
    #     self.prices = self.potions.copy()
    #     with open('test.json', 'r') as f:   # Fetch 
    #         data = json.load(f)
        
    #     for key, ids in self.potions.items():
    #         potion = []
    #         for dose in ids:
    #             try:
    #                 potion.append((data[str(dose)]["avgHighPrice"], data[str(dose)]["avgLowPrice"]))
    #             except KeyError:
    #                 potion.append((None, None))
    #                 continue
    #         self.prices[key] = potion # Replace IDs with prices in dictionary

    #     return

    def three_to_four(self):
        """
        Calculate profit for decanting 3 dose into 4 dose
        """
        profits = []
        for key, value in self.prices.items():  # Loop through prices dictionary
            s3 = value[2][1]    # Grab 3 and 4 dose prices
            b4 = value[3][0]
            if s3 and b4:       # Check that prices are valid
                pass
            else:
                continue
            margin = b4 * 0.75 - s3     # Calculate margin
            profit = int(margin * 2000) # Calculate profit

            if profit >= self.settings.decant_profit_threshold:     # If profit crosses threshold append in dictionary to result list
                add = {"ids": [self.potions[key][2], self.potions[key][3]], "prices": [b4, s3], "limit": 2000, "margin": int(margin), "profit": profit, "roi": fn.get_roi(s3+margin, s3)}
                profits.append(add)
        
        return profits

    def max_profit(self):
        """
        Calculate maximum profit possible from decanting
        """
        profits = []

        for key, value in self.prices.items():
            bppd = []
            sppd = []
            for n in range(4):
                try:
                    bppd.append(value[n][0]/(n+1))
                except TypeError:
                    bppd.append(None)
                try:
                    sppd.append(value[n][1]/(n+1))
                except TypeError:
                    sppd.append(None)

            for n in bppd:
                if n:
                    maxb = [n, bppd.index(n)]
            for n in sppd:
                if n:
                    mins = [n, sppd.index(n)] # Set preliminary max and min prices for potion as well as dose

            for n in range(0,4):    # Find highest price per dose. n: index of potion dose in ID list
                if not bppd[n]:
                    continue
                elif bppd[n] > maxb[0]:
                    maxb = [bppd[n], n]
            for n in range(0,4):    # Find lowest price per dose
                if not sppd[n]:
                    continue
                elif sppd[n] < mins[0]:
                    mins = [sppd[n], n]

            margin = maxb[0] * (maxb[1]+1)*((mins[1]+1)/4)-mins[0]*(mins[1]+1)  # Calculate profit margin
            profit = int(margin * 2000) # Calculate profit

            if profit >= self.settings.decant_profit_threshold:
                add = {"ids": [self.potions[key][mins[1]], self.potions[key][maxb[1]]], "prices": [int(maxb[0]*(maxb[1]+1)), int(mins[0]*(mins[1]+1))], "limit": 2000, "margin": int(margin), "profit": profit, "roi": fn.get_roi(int(mins[0]*(mins[1]+1))+int(margin),int(mins[0]*(mins[1]+1)))}
                profits.append(add)

        return profits

class Cleaning():
    """
    Calculates profit for cleaning items of poison
    """

    pass

class Combine():
    """
    Calculates profit for combining items
    """
    def __init__(self, settings):
        self.settings = settings

        self.items = { # "Product": [Product, part1, part2, ...]
            # Shields
            "Malediction": [11924,11931,11932,11933],
            "Odium": [11926,11928,11929,11930],
            "Dragonfire": [22003, 22006, 1540],
            "AncientWyvern": [21634, 21637, 2890],
            # Spirit shields
            "Elysian": [12817,12819,12831],
            "Spectral": [12821,12823,12831],
            "Arcane": [12825,12827,12831],
            "Blessed": [12831,12833,12829],
            # Boots
            "Primordial": [13239,13231,11840],
            "Pegasian": [13237,13229,2577],
            "Eternal": [13235,13227,6920],
            "Devout": [22954,22960,12598],
            "Brimstone": [22951,22957,23037],
            # Page sets
            "Balance": [13153,3835,3836,3837,3838],
            "Darkness": [13159,12621,12622,12623,12624],
            "Law": [13157,12617,12618,12619,12620],
            "War": [13155,12613,12614,12615,12616],
            "Holy": [13149,3827,3828,3829,3830],
            "Unholy": [13151,3831,3832,3833,3834],
            # Barrows sets
            "Ahrim": [12881,4708,4712,4714,4710],
            "Dharok": [12877,4716,4720,4722,4718],
            "Guthan": [12873,4724,4728,4730,4726],
            "Karil": [12883,4732,4736,4738,4734],
            "Torag": [12879,4745,4749,4751,4747],
            "Verac": [12875,4753,4757,4759,4755],
            # God sets
            "Ancient_lg": [13060,12466,12460,12462,12468],
            "Ancient_sk": [13062,12466,12460,12464,12468],
            "Armadyl_lg": [13052,12476,12470,12472,12478],
            "Armadyl_sk": [13054,12476,12470,12474,12478],
            "Bandos_lg": [13056,12486,12480,12482,12488],
            "Bandos_sk": [13058,12486,12480,12484,12488],
            "Guthix_lg": [13048,2673,2669,2671,2675],
            "Guthix_sk": [13050,2673,2669,3480,2675],
            "Saradomin_lg": [13040,2665,2661,2663,2667],
            "Saradomin_sk": [13042,2665,2661,3479,2667],
            "Zamorak_lg": [13044,2657,2653,2655,2659],
            "Zamorak_sk": [13046,2657,2653,3478,2659],
            # League sets
            "Trailblazer_t1": [25380,25028,25031,25034,25037],
            "Trailblazer_t2": [25383,25016,25019,25022,25025],
            "Trailblazer_t3": [25386,25001,25004,25007,25010],
            "Twisted_t1": [24469,24405,24407,24409,24411],
            "Twisted_t2": [24472,24397,24399,24401,24403],
            "Twisted_t3": [24475,24387,24389,24391,24393],
            # Gold trimmed
            "Bronze_lgg": [12968,12211,12205,12207,12213],
            "Bronze_skg": [12970,12211,12205,12209,12213],
            "Iron_lgg": [12980,12241,12235,12237,12243],
            "Iron_skg": [12982,12241,12235,12239,12243],
            "Steel_lgg": [20382,20178,20169,20172,20181],
            "Steel_skg": [20385,20178,20169,20175,20181],
            "Black_lgg": [12996,2595,2591,2593,2597],
            "Black_skg": [12998,2595,2591,3473,2597],
            "Mithril_lgg": [13008,12283,12277,12279,12281],
            "Mithril_skg": [13010,12283,12277,12285,12281],
            "Adamant_lgg": [13020,2613,2607,2609,2611],
            "Adamant_skg": [13022,2613,2607,3475,2611],
            "Rune_lgg": [13032,2619,2615,2617,2621],
            "Rune_skg": [13034,2619,2615,3476,2621],
            "Gilded_lg": [13036,3486,3481,3483,3488],
            "Gilded_sk": [13038,3486,3481,3485,3488],
            "Gilded_dh": [23124,23264,23267,23261],
            # Trimmed
            "Bronze_lg": [12964,12221,12215,12217,12223],
            "Bronze_sk": [12966,12221,12215,12219,12223],
            "Iron_lg": [12976,12231,12225,12227,12233],
            "Iron_sk": [12978,12231,12225,12229,12233],
            "Steel_lg": [20376,20193,20184,20187,20196],
            "Steel_sk": [20379,20193,20184,20190,20196],
            "Black_lg": [12992,2587,2583,2585,2589],
            "Black_sk": [12994,2587,2583,3472,2589],
            "Mithril_lg": [13004,12293,12287,12289,12291],
            "Mithril_sk": [13006,12293,12287,12295,12291],
            "Adamant_lg": [13016,2605,2599,2601,2603],
            "Adamant_sk": [13018,2605,2599,3474,2603],
            "Rune_lg": [13028,2627,2623,2625,2629],
            "Rune_sk": [13030,2627,2623,3477,2629],
            # Blessed dhide
            "Guthix_dh": [13165,10382,10378,10380,10376],
            "Saradomin_dh": [13163,10390,10386,10388,10384],
            "Zamorak_dh": [13161,10374,10370,10372,10368],
            "Ancient_dh": [13171,12496,12492,12494,12490],
            "Armadyl_dh": [13169,12512,12508,12510,12506],
            "Bandos_dh": [13167,12504,12500,12502,12498],
            # Mystic
            "Blue": [23113,4089,4091,4093,4095,4097],
            "Light": [23110,4109,4111,4113,4115,4117],
            "Dark": [23116,4099,4101,4103,4105,4107],
            "Dusk": [23119,23047,23050,23053,23056,23059],
            # Other sets
            "Dragonstone": [23667,24034,24046,24037,24040,24043],
            "Inquisitor": [24488,24419,24420,24421],
            "Justiciar": [22438,22326,22327,22328],
            "Obsidian": [21279,21298,21301,21304],
            "Cannon": [12863,6,8,10,12],
            "Partyhat": [13173,1038,1040,1042,1044,1046,1048],
            "Halloween": [13175,1053,1055,1057],
            "Ancestral": [21049,21018,21021,21024],
            "Dagonhai": [24333,24288,24291,24294]
        }
    
    # def get_prices(self):
    #     """
        
    #     """
    #     prices = self.items.copy() # Copy dict to change IDs into prices
    #     with open('test.json', 'r') as f:
    #         data = json.load(f)
    #     for key, ids in prices.items(): # Iterate through dict
    #         lst = []            # New list to replace one in dictionary
    #         for n in ids:       # Iterate through list in dict
    #             try:
    #                 if n == 0:
    #                     lst.append((data[str(n)]["avgHighPrice"]))
    #                 else:
    #                     lst.append((data[str(n)]["avgLowPrice"]))
    #             except KeyError:
    #                 lst.append(None)
    #                 continue
    #         prices[key] = lst

    #     return prices

    def combine_profit(self):
        """
        Calculate profits for combine operations
        """
        prices = fn.get_prices(self.items.copy())
        profits = []
        for set in prices.items():
            if None in set[1]:
                continue
            margin = set[1][0] - sum(set[1][1:])
            limit = fn.get_min_limit(self.items[set[0]][1:])
            if not limit:   # If no buy limit
                profit = None
            else:
                profit = limit * margin
            if (profit == None or profit >= self.settings.combine_profit_threshold) and margin >= self.settings.combine_margin_threshold:
                roi = fn.get_roi(set[1][0], sum(set[1][1:]))
                add = {"ids": self.items[set[0]], "prices": prices[set[0]], "limit": limit, "margin": margin, "profit": profit, "roi": roi}
                profits.append(add)
            
        return profits
    
    # def get_limit(self, ids):
    #     """
    #     Get smallest buy limit out of needed items
    #         ids: list of item ids
    #     """
    #     data = fn.get_metadata(ids, limit=True)
    #     limit_dicts = list(data.values())
    #     limits = []
    #     for dict in limit_dicts:
    #         limits.append(dict["limit"])
    #     if None in limits:
    #         return None
    #     else:
    #         return min(limits)

class Pay():
    """
    Calculates profit for paying for services (crushing, unfs).
    """
    def __init__(self, settings):
        self.settings = settings

        self.unfs = {
            # Unfinished potions 200gp
            "avantoe":              [103,261,227],
            "cadantine":            [107,265,227],
            "dwarfWeed":            [109,267,227],
            "guam":                 [91,249,227],
            "harralander":          [97,255,227],
            "irit":                 [101,259,227],
            "kwuarm":               [105,263,227],
            "lantadyme":            [2483,2481,227],
            "marrentill":           [93,251,227],
            "ranarr":               [99,257,227],
            "snapdragon":           [3004,3000,227],
            "tarromin":             [95,253,227],
            "toadflax":             [3002,2998,227],
            "torstol":              [111,269,227],
            "cadantineBlood":       [22443,265,22446]
        }
        self.crush = {
            # Crushing 50gp
            "guamC":                [6681,249],
            "unicornHorn":          [235,237],
            "blueDragonScale":      [241,243],
            "kebbitTeeth":          [10111,10109],
            "birdNest":             [6693,5075],
            "desertGoatHorn":       [9736,9735],
            "chocolateBar":         [1975,1973],
            "lavaScale":            [11994,11992],
            "superiorDragonBones":  [21975,22124]
        }

        # Get prices
        self.unfs_prices = fn.get_prices(self.unfs.copy())
        self.crush_prices = fn.get_prices(self.crush.copy())

    def unfinished_potions_profit(self):
        """
        Function for calculating profits for creating unfinished potions with zahur
        """
        profits = []
        cost = 200
        for key, prices in self.unfs_prices.items():
            margin = prices[0] - (sum(prices[1:]) + cost)
            limit = fn.get_min_limit(self.unfs[key][1:])
            profit = margin * limit
            if profit >= self.settings.pay_profit_threshold:
                profits.append({"ids": self.unfs[key], "prices": prices, "limit": limit, "margin": margin, "profit": profit, "roi": fn.get_roi(prices[0], (sum(prices[1:]) + cost))})
        return profits

    def crush_profit(self):
        """
        Function for calculating profits for crushing items with wesley
        """
        cost = 50
        return

class Repair():
    """
    Calculates profit for repairing barrows armor at an armour stand.
    """
    def __init__(self, settings):
        self.settings = settings

        items = {

        }