#! /usr/bin/env python2

import urllib2
import json
import copy
from xivsettings import *
from GearItem import *

categories = [
["Arm", "Grimoire"],
["Head",],
["Body",],
["Hands",],
["Waist",],
["Legs",],
["Feet",],
["Necklace",],
["Earrings",],
["Bracelets",],
["Ring",],
]
stat_names = ["AP", "ACC", "CRIT", "DET", "SS", "VIT", "WepDmg", "WepDelay"]

def pprintjson(jsonstuff):
    print json.dumps(jsonstuff, sort_keys=True, indent=4, separators=(',', ': '))

def getQueryResponse(url):
    return json.loads(urllib2.urlopen(url).read())

def generateRawItem(item):
    # tries to generate item in the format
    # [[DEX, ACC, CRIT, DET, SKILLSPEED, VIT, WEAPONDAMAGE, WEAPONDELAY], "Item Name"]
    # also returns some additional informatoin [numberofmeld slots, gear type, item level, is_unique]
    stats = {
            cJob.AttributeName():0,
            "Vitality":0,
            "Accuracy":0,
            "Determination":0,
            cJob.SSName():0,
            "Critical Hit Rate":0,
            "Parry":0,
            "Piety":0,
            }
    detailedItem = getQueryResponse(item["url_api"])
    # pprintjson(detailedItem)
    # print detailedItem["name"]
    if detailedItem["craftable"] != None and detailedItem["craftable"] != [] and overmeld > 0:
        # print detailedItem["craftable"]
        overmeldable = True
    else:
        overmeldable = False
    meldslots = detailedItem["materia_slot_count"]
    # print detailedItem
    for attribute in detailedItem["attributes_params"]:
        stats[attribute["name"]] = max(attribute["value"], attribute["value_hq"])
    attributes_base = detailedItem["attributes_base"]
    WEAPONDAMAGE = max(attributes_base[cJob.damageType()], attributes_base[cJob.damageType()+"_hq"])
    WEAPONDELAY = max(attributes_base["delay"], attributes_base["delay_hq"])
    itemlevel = detailedItem["level_item"]
    geartype = detailedItem["category_name"]
    itemid = detailedItem["id"]
    # isunique = detailedItem["is_unique"]
    if detailedItem["craftable"] != None and detailedItem["craftable"] != []:
        # print detailedItem["craftable"]
        isunique = 0
    else:
        isunique = 1
    # print detailedItem["name"].encode("ascii", "ignore")
    return GearItem(stats[cJob.AttributeName()], stats["Accuracy"], stats["Critical Hit Rate"], stats["Determination"], stats[cJob.SSName()], stats["Vitality"], WEAPONDAMAGE, WEAPONDELAY, detailedItem["name"].replace("'", "").replace("-",""), meldslots, geartype, itemlevel, isunique, itemid, cJob.attributeval, overmeldable, stats["Parry"], stats["Piety"])


def equip_slot_category_map(items):
    for item in items:
        detailedItem = getQueryResponse(item["url_api"])
        print detailedItem["category_name"], detailedItem["equip_slot_category"], detailedItem["name"]

def categorize_items(items):
    item_sorted = [[] for _ in xrange(len(categories))]
    for item in items:
        gitem = generateRawItem(item)
        for i in range(0, len(categories)):
            for categorie in categories[i]:
                if categorie in gitem.geartype:
                    item_sorted[i].append(gitem)
                # else:
                #     print categorie, gitem.geartype
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
            if item.itemlevel not in caps:
                caps[item.itemlevel] = [[0,0], [0,0], [0,0], [0,0]]
            # find the high stat
            # stat_names
            highstat = 0
            highstat_index = 0
            for i in range(1, 5):
                if item.stats[i] > highstat:
                    highstat = item.stats[i]
                    highstat_index = i
            highstat_index = statslot_to_capslot(highstat_index)
            item_type = item.geartype
            caps[item.itemlevel][item_type_to_index(item_type)][highstat_index] = highstat
    for key in caps:
        for group in caps[key]:
            for i in range(len(group)):
                if group[i] == 0:
                    group[i] = key
    return caps

def generateMeldedVersions(item, statweights, caps):
    accmelds = 0
    mycaps = caps[item.itemlevel]
    materiamax = 12
    # TODO handle det melds
    # while we have done less acc melds than there are slots
    itemnames = []
    if item.overmeldable:
        meldslots = min(5, item.meldslots+overmeld)
    else:
        meldslots = item.meldslots
    while accmelds <= meldslots:
        meldchoices = ""
        item_copy = copy.deepcopy(item)
        if doDamageMelds:
            # meld the non accuracy slots
            for i in range(0, meldslots - accmelds):
                bestmeldstats = 0
                bestmeldslot = 0
                if cJob.attributeval == 3 and i == 0 and item.stats[0] == 0:
                    bestmeldstats = 0
                    bestmeldstats = 15
                    materiamax = 15
                else:
                    for slot in range(2,5):
                        # determine the meld amount to use
                        if item.itemlevel < minVmeldlevel or i - item.meldslots >= overmeldVcount:
                            if slot == 1 or slot == 2 or slot == 4:
                                materiamax = 9
                            elif slot == 3:
                                materiamax = 6
                        else:
                            materiamax = 12
                        availstats = min(materiamax, mycaps[item_type_to_index(item.geartype)][statslot_to_capslot(slot)] -item_copy.stats[slot])
                        if availstats*statweights[slot] > bestmeldstats*statweights[bestmeldslot]:
                            bestmeldstats = availstats
                            bestmeldslot = slot
                item_copy.stats[bestmeldslot] += bestmeldstats
                meldchoices += "+" + stat_names[bestmeldslot] + str(bestmeldstats)
        else:
            accmelds = meldslots
        for i in range(0, accmelds):
            availstats = min(materiamax, mycaps[item_type_to_index(item.geartype)][0] - item_copy.stats[1])
            item_copy.stats[1] += availstats
            meldchoices += "+" + stat_names[1] + str(availstats)
            if availstats == 0:
                return itemnames
        varname = item_copy.name.replace(" ", "_") + str(accmelds)
        item_copy.name += meldchoices
        item_list = [item_copy.stats, item_copy.name]
        # if "Ring" in item_copy.geartype:
        item_list.append(item_copy.isunique)
        item_list.append(item_copy.itemid)
        print varname + " = " + str(item_list)
        accmelds = accmelds + 1
        if not item_copy.itemlevel > maxdefaultobtainedlvl:
            itemnames.append(varname)
    return itemnames

# TODO make this into a main function
url = cJob.gearQuery(minlevel)

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
# for cat in items_sorted:
#     for item in cat:
#         print item

caps = determine_caps(items_sorted)
# print caps

i = 0
catnames = []
for item_cat in items_sorted:
    catname = categories[i][0]
    if catname == "Ring":
        catnames.append(catname)
    catnames.append(catname)
    itemnames = []
    for item in item_cat:
        itemnames += generateMeldedVersions(item, cJob.weights, caps)
    print catname + " = [",
    for itemname in itemnames:
        print itemname + ",",
    print "]"
    print
    print
    i += 1
