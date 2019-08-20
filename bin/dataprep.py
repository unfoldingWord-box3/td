import json
import os
import re # for data subsetting
import yaml
import csv

basedirflag = True
if not os.path.exists("./data") : basedirflag = False
if not os.path.exists("./docs") : basedirflag = False
if not os.path.exists("./bin") : basedirflag = False

if not basedirflag :
    print ("Note: this script should be run in the project root folder:")
    print ("Thus: python3 bin/dataprep.py")
    print ("These subdirs must exist: data, docs, and bin")
    exit()

# create the "docs/languages"
docslangpath = "./docs/languages"
if not os.path.exists(docslangpath):
    try:
        os.mkdir(docslangpath)
    except OSError:
        print ("Creation of directory %s failed" % docslangpath)
        exit()
    else:
        print ("Successfully created directory %s " % docslangpath)

#
# open and parse iso-639-3 tab separated values file
# 3 letter code is first column; 2 letter code (if any) is fourth
#
i639_dict = {}
with open("data/iso-639-3.tsv", newline = '') as iso_639_file:
    i639 = csv.reader(iso_639_file, delimiter='\t')
    for row in i639:
        if row[3] == "":
            i639_dict[row[0]] = row[0]
        else:
            i639_dict[row[3]] = row[0]

#
# country code to name lookup
#
cc_dict = {}
with open("data/cc.csv") as cc_file:
    cc = csv.reader(cc_file)
    for row in cc:
        if len(row[0]) == 0:
            continue
        cc_dict[row[0]] = row[1]

#
# open and parse the all languages JSON
#
with open("data/langnames.json", "r") as lnfile:
    lndata = lnfile.read()
    jlndata = json.loads(lndata)

#
# open and parse the gateway languages JSON
#
with open("data/ln_gw.json", "r") as gwfile:
    gwdata = gwfile.read()
    jgwdata = json.loads(gwdata)

# load up the dictionary for lang and gw
count=0
gwdict = {}
for gwj in jgwdata:
    count = count+1
    gwdict[gwj["lc_code"]] = gwj["gw_code"]

print("\n\n\nTotal in ln/gw list: "+str(count))

count=0
for lnj in jlndata:
    count=count+1
    lc = lnj["lc"] # here is the language code
    #print (lc)
    ### DEBUG CODE ###
    ### only actually create a few language dirs
    #tomatch = "^(ca|en|es|gaj|dnr|tpi)$"
    #ismatch = re.search(tomatch, lc)
    #if (not ismatch) : 
    #    continue

    # lookup the gateway language
    try:
        gwcode = gwdict[lc]
    except KeyError:
        print ("No gateway language for "+lc)
        gwcode = "UNKNOWN"
    #else:
    #    print ("Gateway language for "+lc+" is "+str(gwcode))

    # add it to the language data
    lnj["gwcode"] = gwcode

    # lookup the iso-639-3 code
    try:
        i639_code = i639_dict[lc]
    except KeyError:
        #print ("No ISO 639-3 code for "+lc)
        i639_code = "UNKNOWN"
    #else:
    #    print ("ISO 639-3 code for "+lc+" is "+str(i639_code))

    # add ISO 639-3 to the language data
    lnj["ISO-639-3"] = i639_code

    # create lang subdir if needed
    path = docslangpath + "/" + lc
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of directory %s failed" % path)
            exit()
        else:
            print ("Successfully created directory %s " % path)
    
    # now print the lang json to "lc".json
    fpath = path + "/" + lc + ".json"
    with open(fpath,"w") as fpath_handle:
        json.dump(lnj,fpath_handle, indent=4)

    # next write the YAML to "lc".yaml
    #fpath = path + "/" + lc + ".yaml"
    #with open(fpath,"w") as ypath_handle:
    #    yaml.dump(lnj,ypath_handle,allow_unicode=True, default_flow_style=False)

    # some boilerplate
    note_a = ".. note:: The `Ethnologue <https://www.ethnologue.com/language/"
    note_b = ">`_ identifies this language as ``"
    note_c = "``."

    # human friendly key mapping
    friendlyKeys = {"lc":"lang_code",
        "ISO-639-3":"ISO_639-3",
        "ln":"lang_name",
        "ang":"anglicanized_name",
        "alt":"alternate_names",
        "ld":"lang_direction",
        "gwcode":"gateway_language",
        "lr":"lang_region",
        "cc":"country_codes",
        }
    # next write the "lc".rst page
    fpath = path + "/" + lc + ".rst"
    with open(fpath,"w") as rst:
        rst.write(".. _%s:\n\n" % lc)
        ln = lnj["ln"]
        uln = ln.encode("utf-8")
        rst.write("%s\n%s\n\n" % (lnj["ln"], ('=' * len(uln))))
        if len(lc) == 2:
            i639_code = lnj["ISO-639-3"]
            rst.write("%s%s%s%s%s\n\n" % (note_a,i639_code,note_b,i639_code,note_c))
        rst.write("This language is spoken in the following countries:\n\n")
        for i in lnj["cc"]:
            rst.write("* %s: %s\n" % (i,cc_dict[i]))
        rst.write("\n")
        friendlyMap = {}
        for i in friendlyKeys:
            friendlyMap[friendlyKeys[i]] = lnj[i]
        rst.write(".. code-block:: yaml\n\n")
        y = yaml.dump(friendlyMap,allow_unicode=True, default_flow_style=False)
        for line in y.split('\n'):
            rst.write("%s%s\n" % ("    ", line))



print("\n\n\nTotal in all lang list: "+str(count))