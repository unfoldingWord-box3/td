import json
import os
import re # for data subsetting
import yaml

basedirflag = True
if not os.path.exists("./data") : basedirflag = False
if not os.path.exists("./docs") : basedirflag = False
if not os.path.exists("./bin") : basedirflag = False

if not basedirflag :
    print ("Note: this script should be run in the project root folder:")
    print ("Thus: python3 bin/dataprep.py")
    print ("These subdirs must exist: data, docs, and bin")
    exit()

# create the "data/languages"
datalangpath = "./data/languages"
if not os.path.exists(datalangpath):
    try:
        os.mkdir(datalangpath)
    except OSError:
        print ("Creation of directory %s failed" % datalangpath)
        exit()
    else:
        print ("Successfully created directory %s " % datalangpath)

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
    tomatch = "^(ca|en|es|gaj|dnr|tpi)$"
    ismatch = re.search(tomatch, lc)
    if (not ismatch) : 
        continue

    # lookup the gateway language
    try:
        gwcode = gwdict[lc]
    except KeyError:
        print ("No gateway language for "+lc)
        gwcode = "UNKNOWN"
    else:
        print ("Gateway language for "+lc+" is "+str(gwcode))

    # add it to the language data
    lnj["gwcode"] = gwcode

    # create lang subdir if needed
    path = datalangpath + "/" + lc
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
    fpath = path + "/" + lc + ".yaml"
    with open(fpath,"w") as ypath_handle:
        yaml.dump(lnj,ypath_handle,allow_unicode=True, default_flow_style=False)



print("\n\n\nTotal in all lang list: "+str(count))