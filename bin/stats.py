import json
import os

basedirflag = True
if not os.path.exists("./data") : basedirflag = False
if not os.path.exists("./docs") : basedirflag = False
if not os.path.exists("./bin") : basedirflag = False

if not basedirflag :
    print ("Note: this script should be run in the project root folder:")
    print ("Thus: python3 bin/dataprep.py")
    print ("These subdirs must exist: data, docs, and bin")
    exit()

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


count=0
lr_dict_count = {}
gw_dict_count = {}
for lnj in jlndata:
    count=count+1
    lc = lnj["lc"] # here is the language code
    lr = lnj["lr"] # here is the language code
    if lr == "":
        lr="UNKNOWN"

    # lookup the gateway language
    try:
        gwcode = gwdict[lc]
    except KeyError:
        gwcode = "UNKNOWN"

    if str(gwcode) == "None":
        gwcode = "Missing"

    try:
        temp_count = lr_dict_count[lr]
        lr_dict_count[lr] = temp_count + 1
    except KeyError:
        lr_dict_count[lr] = 1

    if lnj["gw"]:
        continue

    try: 
        temp_count = gw_dict_count[gwcode]
        gw_dict_count[gwcode] = temp_count + 1
    except KeyError:
        gw_dict_count[gwcode] = 1


print("\n\n")
print("=============== Summary ===============")
print("        Total number of languages: %i" % count)
print("          Total number of regions: %i" % len(lr_dict_count))
print("Total number of gateway languages: %i" % len(gw_dict_count))
print("\n\n")

print("===== Languages per Region =====")
for i in sorted(lr_dict_count.keys()):
    print("%s:%i" % (i,lr_dict_count[i]))

print("\n\n")
print("===== Languages per G/L =====")
for i in sorted(gw_dict_count.keys()):
    print("%s:%i" % (i,gw_dict_count[i]))
