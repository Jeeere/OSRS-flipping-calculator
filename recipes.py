"""
Includes recipes used in flipping
"""
import json

class Decant():
    """
    Calculates profit for decanting potions
    bn, sn: buy and sell prices for n dose potion
    """
    def __init__(self):
        self.profit_threshold = 100000

        self.potions = {#"Potion":  [1dose,2dose,3dose,4dose],
                    "Agility":      [3038,3036,3034,3032],
                    "Antifire":     [2458,2456,2454,2452],
                    "Attack":       [125,123,121,2428],
                    "Bastion":      [22470,22467,22464,22461],
                    "Battlemage":   [22458,22455,22452,22449],
                    "Combat":       [9745,9743,9741,9739],
                    "Compost":      [6476,6474,6472,6470],
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

    def get_prices(self):
        """
        Get prices for all tradeable potions
        """
        prices = self.potions
        with open('test.json', 'r') as f:
            data = json.load(f)
            items = data["data"]
        for key, ids in self.potions.items():
            potion = []
            for dose in ids:
                try:
                    potion.append((items[str(dose)]["avgHighPrice"], items[str(dose)]["avgLowPrice"]))
                except KeyError:
                    potion.append((None, None))
                    continue
            prices[key] = potion
            if potion[2][1] and potion[3][0]:
                self.three_to_four(key, potion[2][1], potion[3][0])
        return

    def three_to_four(self, key, s3, b4):
        """
        Calculate profit for decanting 3 dose into 4 dose
        """
        margin = b4 * 0.75 - s3
        profit = int(margin * 2000)
        if profit >= self.profit_threshold:
            print(key + " potions have a 3to4 profit of " + f'{profit:,}' + " with Buy: " + f'{s3:,}' + " Sell: " + f'{b4:,}')
            return profit, s3, b4
        else:
            return

    def max_profit(b1, s1, b2, s2, b3, s3, b4, s4):
        """
        Calculate maximum profit possible from decanting
        """
        bppd = [b1, int(b2/2), int(b3/3), int(b4/4)]
        sppd = [s1, int(s2/2), int(s3/3), int(s4/4)]
        maxb = [bppd[0], 1]
        mins = [sppd[0], 1]
        for n in range(1,4):
            if bppd[n] > maxb[0]:
                maxb = [bppd[n], n+1]
        for n in range(1,4):
            if sppd[n] < mins[0]:
                mins = [sppd[n], n+1]
        margin = maxb[0] * maxb[1]*(mins[1]/4)-mins[0]*mins[1]
        profit = int(margin * 2000)
        return margin, profit

class Cleaning():
    """
    Calculates profit for cleaning items of poison
    """

    pass

class Combine():
    """
    Calculates profit for combining items
    """
    def __init__(self):
        self.profit_threshold = 100000

        items = { # "Product": [Product, part1, part2, ...]
            # Wards
            "Malediction": [11924,11931,11932,11933],
            "Odium": [11926,11928,11929,11930],
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
            "Ancient_lg": [],
            "Ancient_sk": [],
            "Armadyl_lg": [],
            "Armadyl_sk": [],
            "Bandos_lg": [],
            "Bandos_sk": [],
            "Guthix_lg": [],
            "Guthix_sk": [],
            "Saradomin_lg": [],
            "Saradomin_sk": [],
            "Zamorak_lg": [],
            "Zamorak_sk": [],
            # League sets
            "Trailblazer_t1": [],
            "Trailblazer_t2": [],
            "Trailblazer_t3": [],
            "Twisted_t1": [],
            "Twisted_t2": [],
            "Twisted_t3": [],
            # Gold trimmed
            "Bronze_lgg": [],
            "Bronze_skg": [],
            "Iron_lgg": [],
            "Iron_skg": [],
            "Steel_lgg": [],
            "Steel_skg": [],
            "Black_lgg": [],
            "Black_skg": [],
            "Mithril_lgg": [],
            "Mithril_skg": [],
            "Adamant_lgg": [],
            "Adamant_skg": [],
            "Rune_lgg": [],
            "Rune_skg": [],
            "Gilded_lg": [13036,3486,3481,3483,3488],
            "Gilded_sk": [13038,3486,3481,3485,3488],
            "Gilded_dh": [],
            # Trimmed
            "Bronze_lg": [],
            "Bronze_sk": [],
            "Iron_lg": [],
            "Iron_sk": [],
            "Steel_lg": [],
            "Steel_sk": [],
            "Black_lg": [],
            "Black_sk": [],
            "Mithril_lg": [],
            "Mithril_sk": [],
            "Adamant_lg": [],
            "Adamant_sk": [],
            "Rune_lg": [],
            "Rune_sk": [],
            # Blessed dhide
            "Guthix_dh": [],
            "Saradomin_dh": [],
            "Zamorak_dh": [],
            "Ancient_dh": [],
            "Armadyl_dh": [],
            "Bandos_dh": [],
            # Mystic
            "Blue": [],
            "Light": [],
            "Dark": [],
            "Dusk": [],
            # Other sets
            "Dragonstone": [23667,24034,24046,24037,24040,24043],
            "Inquisitor": [],
            "Justiciar": [],
            "Obsidian": [],
            "Cannon": [],
            "Partyhat": [],
            "Halloween": [],
            "Ancestral": [],
            "Dagonhai": []
        }
    
    def get_prices(self):
        return

    def combine_profit(self):
        return

class GildedSets():
    """
    
    """
    pass