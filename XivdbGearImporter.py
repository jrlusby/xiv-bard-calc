#! /usr/bin/env python2

import urllib2
import json
import copy

categories = ["Arm", "Head", "Body", "Hands", "Waist", "Legs", "Feet", "Necklace", "Earrings", "Bracelets", "Ring", "Ring"]
stat_names = ["DEX", "ACC", "CRIT", "DET", "SKS", "VIT", "WepDmg", "WepDelay"]
stat_weights = [1.0, 0, .300, .166, .166, 0, 13.459, 0]

def pprintjson(jsonstuff):
    print json.dumps(jsonstuff, sort_keys=True, indent=4, separators=(',', ': '))

def getQueryResponse(url):
    return json.loads(urllib2.urlopen(url).read())

def generateRawItem(item):
    # tries to generate item in the format
    # [[DEX, ACC, CRIT, DET, SKILLSPEED, VIT, WEAPONDAMAGE, WEAPONDELAY], "Item Name"]
    # also returns some additional informatoin [numberofmeld slots, gear type, item level, is_unique]
    stats = {
            "Dexterity":0,
            "Vitality":0,
            "Accuracy":0,
            "Determination":0,
            "Skill Speed":0,
            "Critical Hit Rate":0,
            }
    detailedItem = getQueryResponse(item["url_api"])
    # pprintjson(detailedItem)
    if detailedItem["craftable"] == []:
        meldslots = detailedItem["materia_slot_count"]
    else:
        meldslots = 5
    # print detailedItem
    for attribute in detailedItem["attributes_params"]:
        stats[attribute["name"]] = max(attribute["value"], attribute["value_hq"])
    attributes_base = detailedItem["attributes_base"]
    WEAPONDAMAGE = max(attributes_base["damage"], attributes_base["damage_hq"])
    WEAPONDELAY = max(attributes_base["delay"], attributes_base["delay_hq"])
    itemlevel = detailedItem["level_item"]
    geartype = detailedItem["category_name"]
    # isunique = detailedItem["is_unique"]
    if meldslots == 5:
        isunique = 0
    else:
        isunique = 1
    return [[stats["Dexterity"], stats["Accuracy"], stats["Critical Hit Rate"], stats["Determination"], stats["Skill Speed"], stats["Vitality"], WEAPONDAMAGE, WEAPONDELAY], detailedItem["name"]], [meldslots, geartype, itemlevel, isunique]

def equip_slot_category_map(items):
    for item in items:
        detailedItem = getQueryResponse(item["url_api"])
        print detailedItem["category_name"], detailedItem["equip_slot_category"], detailedItem["name"]

def categorize_items(items):
    item_sorted = [[] for _ in xrange(len(categories))]
    for item in items:
        itemstats, itemmeta = generateRawItem(item)
        for i in range(0, len(categories)):
            if categories[i] in itemmeta[1]:
                item_sorted[i].append([itemstats, itemmeta])
    return item_sorted

def statslot_to_capslot(statslot):
    if statslot == 3:
        return 1
    else:
        return 0

def item_type_to_index(item_type):
    if "Arm" in item_type:
        return 0
    elif "Body" in item_type or "Legs" in item_type:
        return 1
    elif "Head" in item_type or "Hands" in item_type or "Feet" in item_type:
        return 2
    else:
        return 3

# expects items of the format output by generateRawItem
# [[weaponcaps], [bodylegscaps], [headglovesfeetcaps], [waistaccessorycaps]]
def determine_caps(items):
    caps = {}
    for item_category in items:
        for item in item_category:
            if item[1][2] not in caps:
                caps[item[1][2]] = [[0,0], [0,0], [0,0], [0,0]]
            # find the high stat
            # stat_names
            highstat = 0
            highstat_index = 0
            for i in range(1, 5):
                if item[0][0][i] > highstat:
                    highstat = item[0][0][i]
                    highstat_index = i
            highstat_index = statslot_to_capslot(highstat_index)
            item_type = item[1][1]
            caps[item[1][2]][item_type_to_index(item_type)][highstat_index] = highstat
    return caps

def generateMeldPriorities(statweights):
    priorities = []
    for i in range(2,5):
        maxstat = i
        for j in range(2,5):
            if j not in priorities and statweights[j] > statweights[maxstat]:
                maxstat = j
        priorities.append(maxstat)
    return priorities


def generateMeldedVersions(item, statweights, caps):
    accmelds = 0
    mycaps = caps[item[1][2]]
    # while we have done less acc melds than there are slots
    itemnames = []
    while accmelds <= item[1][0]:
        meldchoices = ""
        item_copy = copy.deepcopy(item)
        # meld the non accuracy slots
        for i in range(0, item[1][0] - accmelds):
            bestmeldstats = 0
            bestmeldslot = 0
            for slot in range(2,5):
                availstats = min(12, mycaps[item_type_to_index(item[1][1])][statslot_to_capslot(slot)] -item_copy[0][0][slot])
                if availstats*statweights[slot] > bestmeldstats*statweights[bestmeldslot]:
                    bestmeldstats = availstats
                    bestmeldslot = slot
            item_copy[0][0][bestmeldslot] += bestmeldstats
            meldchoices += "+" + stat_names[bestmeldslot] + str(bestmeldstats)
        for i in range(0, accmelds):
            availstats = min(12, mycaps[item_type_to_index(item[1][1])][0] - item_copy[0][0][1])
            item_copy[0][0][1] += availstats
            meldchoices += "+" + stat_names[1] + str(availstats)
            if availstats == 0:
                return itemnames
        varname = item_copy[0][1].replace(" ", "_") + str(accmelds)
        item_copy[0][1] += meldchoices
        if "Ring" in item_copy[1][1]:
            item_copy[0].append(item_copy[1][3])
        print varname + " = " + str(item_copy[0])
        accmelds = accmelds + 1
        itemnames.append(varname)
    return itemnames


# url = "https://api.xivdb.com/search?string=Torrent,Aiming"
# url = "https://api.xivdb.com/item/14336"
url = "https://api.xivdb.com/search?classjobs=31&one=items&level_item%7Cgt=220&attributes=2%7Cgt%7C1%7C0&language=en"

next_page = 1
last_page = 1
items = []


while next_page <= last_page:
    c_query = getQueryResponse(url+"&page="+str(next_page))
    next_page = c_query["items"]["paging"]["next"]
    last_page = c_query["items"]["paging"]["total"]
    items = items + c_query["items"]["results"]

# pprintjson(items)
# equip_slot_category_map(items)
items_sorted = categorize_items(items)
# pprintjson( items_sorted[11])

caps = determine_caps(items_sorted)

i = 0
catnames = []
for item_cat in items_sorted:
    catname = categories[i]
    if catname == "Ring":
        catname += str(i - 10)
    catnames.append(catname)
    itemnames = []
    print
    print
    for item in item_cat:
        itemnames += generateMeldedVersions(item, stat_weights, caps)
    print catname + " = [",
    for itemname in itemnames:
        print itemname + ",",
    print "]"
    i += 1

# TODO pull food from xivdb or something
print "food = [flintcaviar]"
catnames.append("food")

print "allitems = [",
for catname in catnames:
    print catname + ",",
print "]"
