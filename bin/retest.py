import re

tomatch="ca|en|dnr"

ismatch=re.search(tomatch,"en")

if not ismatch :
    print ("no")
else:
    print ("yes")