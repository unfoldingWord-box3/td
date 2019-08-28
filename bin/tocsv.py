import json
import os
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
# open and parse the gateway languages JSON
#
with open("data/ln_gw.json", "r") as gwfile:
    gwdata = gwfile.read()
    jgwdata = json.loads(gwdata)

# load up the dictionary for lang and gw
gwdict = {}
gwvalid = {}
for gwj in jgwdata:
    gwdict[gwj["lc_code"]] = gwj["gw_code"]
    gwvalid[gwj["gw_code"]] = gwj["gateway_flag"]


# write out the csv for ln_gw.json
with open("data/lc_gw.csv", 'w', newline='') as f:
    c1w = csv.writer(f, dialect='excel')
    # write header
    c1w.writerow(['lc','gw','gw_flag'])
    for gwj in jgwdata:
        lc = gwj["lc_code"]
        gw = gwj["gw_code"]
        if gw is None:
            gw = "MISSING"
        gw_flag = gwj["gateway_flag"]
        if gw_flag is None:
            gw_flag = False
        c1w.writerow([lc,gw,gw_flag])


with open("data/langnames.json", "r") as lnfile:
    lndata = lnfile.read()
    jlndata = json.loads(lndata)

#
# augment json with ISO lang codes and the gateway language
#
for lnj in jlndata:
    # lookup the iso-639-3 code
    lc = lnj["lc"]
    try:
        i639_code = i639_dict[lc]
    except KeyError:
        #print ("No ISO 639-3 code for "+lc)
        i639_code = "UNKNOWN"
    # add ISO 639-3 to the language data
    lnj["ISO-639-3"] = i639_code

    # lookup the gateway language
    try:
        gwcode = gwdict[lc]
    except KeyError:
        gwcode = "UNKNOWN"
    #else:
    #    print ("Gateway language for "+lc+" is "+str(gwcode))

    # add it to the language data
    lnj["gwcode"] = gwcode

# write out the language csv (all attributes with 1..1 cardinality)
with open("data/lc.csv",'w', newline='') as f:
    cw = csv.writer(f, dialect='excel')
    # write header
    cw.writerow(['lc','lr','hc','ln','ang','pk','gw','is_gw','iso','ld'])
    for lnj in jlndata:
        lc = lnj["lc"]
        lr = lnj["lr"]
        hc = lnj["hc"]
        ln = lnj["ln"]
        ang = lnj["ang"]
        pk = lnj["pk"]
        gw = lnj["gwcode"]
        is_gw = lnj["gw"]
        iso = lnj["ISO-639-3"]
        ld = lnj["ld"]
        cw.writerow([lc,lr,hc,ln,ang,pk,gw,is_gw,iso,ld])

# write out the language to country codes
with open("data/lc_cc.csv",'w', newline='') as f:
    cw = csv.writer(f, dialect='excel')
    # write header
    cw.writerow(['lc','cc','name'])
    for lnj in jlndata:
        lc = lnj["lc"]
        cc = lnj['cc']
        for c in cc:
            cn = cc_dict[c]
            cw.writerow([lc,c,cn])

# write out the language to alternates
with open("data/lc_alt.csv",'w', newline='') as f:
    cw = csv.writer(f, dialect='excel')
    # write header
    cw.writerow(['lc','alt'])
    for lnj in jlndata:
        lc = lnj["lc"]
        alt = lnj['alt']
        for a in alt:
            cw.writerow([lc,a])



