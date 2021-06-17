import json
from recipes import Combine, Decant

def main(b1,s1,b2,s2,b3,s3,b4,s4):
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
    print("----------")
    print(bppd)
    print("----------")
    print(sppd)
    print("----------")
    print(maxb)
    print("----------")
    print(mins)
    print("----------")
    print(bppd[2])
    print("----------")
    print(maxb[0])
    print("----------")
    margin = maxb[0] * maxb[1]*(mins[1]/4)-mins[0]*mins[1]
    print(margin)

b1,s1,b2,s2,b3,s3,b4,s4 = 2534, 2456, 4946, 4897, 7756, 7755, 10540, 10459
#main(b1,s1,b2,s2,b3,s3,b4,s4)

potions = {#"Potion":  [1dose,2dose,3dose,4dose], 
                    "Agility":      [3038,3036,3034,3032],
                    "Antifire":     [2458,2456,2454,2452],
                    "Attack":       [125,123,121,2428],
                    "Bastion":      [22470,22467,22464,22461],
                    "Battlemage":   [22458,22455,22452,22449],
                    "Combat":       [9745,9743,9741,9739],
                    "Compost":      [6476,6474,6472,6470],
                    "Defence":      [137,135,133,2432],
                    "DBastion":     [24644,24641,24638,24635],
                    "DBattlemage":  [24632,24629,24626,24623],
                    "DMagic":       [23754,23751,23748,23745],
                    "DRanging":     [23742,23739,23736,23733],
                    "DSAttack":     [23706,23703,23700,23697],
                    "DSCombat":     [23694,23691,23688,23685],
                    "DSDefence":    [23730,23727,23724,23721],
                    "DSStrength":   [23718,23715,23712,23709],
                    "Energy":       [3014,3012,3010,3008],
                    "Fishing":      [155,153,151,2438],
                    "Hunter":       [10004,10002,10000,9998],
                    "Magic":        [3046,3044,3042,3040],
                    "Prayer":       [143,141,139,2434],
                    "Ranging":      [173,171,169,2444],
                    "Restore":      [131,129,127,2430],
                    "Stamina":      [12631,12629,12627,12625],
                    "Strength":     [119,117,115,113],
                    "SAntifire":    [21987,21984,21981,21978],
                    "SCombat":      [12701,12699,12697,12695]}
# prices = potions
# with open('test.json', 'r') as f:
#     data = json.load(f)
#     items = data["data"]
# for key, ids in potions.items():
#     potion = []
#     for dose in ids:
#         try:
#             potion.append((items[str(dose)]["avgHighPrice"], items[str(dose)]["avgLowPrice"]))
#         except KeyError:
#             potion.append((None, None))
#             continue
#     print(potion)
#     prices[key] = potion
# #print(prices)

# xd = None
# if xd:
#     print("y")
# else:
#     print("n")

decant = Decant()
#decant.get_prices()

combine = Combine()
#combine.get_prices()

new = {}
with open('test.json', 'r') as f:
            data = json.load(f)
            for key1, dict in data.items():
                new[key1] = {}
                for key2, value in dict.items():
                    if value:
                        new[key1][key2] = value
            

