# translationDatabase

See http://td.rtfd.io/, this repository contains the source files.

If you want to suggest a change, please fork this repo and create a PR, or create an Issue.


## Building

*Note there is now a data preparation step; see below*

Install the sphinx engine

    sudo apt-get install python-sphinx

Then run the build script.

> NOTE: this top level makefile is just a shorcut to building the html.

    make


## Data Preparation

In the data folder are two JSON files which must
be refreshed manually at present. These two JSON
files are inputs `bin/dataprep.py`.

- `data/langnames.json`: this is downloaded from the 
current tD production website as follows:
    - Go to https://td.unfoldingword.org
    - Click "Data Sources", then
    - Click "Language Names JSON"
    - Or use direct link: https://td.unfoldingword.org/langnames.json
- `data/ln_gw.json`: this is created by the following SQL against the tD Postgres database:
    ```sql
    select u.code lc_code,g.code as gw_code 
    from uw_language u 
    left outer join uw_language g 
    on u.gateway_language_id = g.id
    where g.gateway_flag = true
    order by u.code
    ```
    - using DBeaver, the result set is exported as JSON. Exporting notes:
        - Toggle off the setting `Print table name`
        - Use encoding UTF-8
        - Toggle off setting to "Insert BOM"
- `data/iso-639-3.tsv` has mapping between 2 and 3 letter codes. From:
https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab. See below for DDL (intended to be imported into a database table). ISO 639-1 is the two character standard and 639-3 is the three character one.
- `data/cc.csv` has ISO 3166 alpha-2 country codes. This copied from 
https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 and pasted into Excel, then saved as `cc.csv`
- `bin/dataprep.py`: this Python3 script will output:
    - one folder per language (in `data/languages`)
    - each folder will have:
        - the original JSON from `langnames.json` with the addition of a key named "gwcode" and its value. This will be the Gateway Language (if any) for the language.
        - the JSON converted to YAML format

During development there is debug code which restricts actions to 
only a few languages. This is avoid creation of 8K+ directories.

# Stats
Some analysis of input language data is available using the stats script:
```bash
=============== Summary ===============
        Total number of languages: 8703
          Total number of regions: 6
Total number of gateway languages: 44



===== Languages per Region =====
Africa:2331
Americas:1157
Asia:3142
Europe:420
Pacific:1623
UNKNOWN:30



===== Languages per G/L =====
UNKNOWN:594
am:82
ar:319
as:36
bi:18
bn:30
ceb:59
en:1658
es:21
es-419:605
fa:57
fr:1057
gu:15
ha:1
hi:130
id:1035
ilo:76
km:21
kn:51
lo:59
ml:27
mn:3
mr:29
ms:129
my:105
ne:104
or:18
pa:3
plt:12
pmy:8
ps:31
pt:267
pt-br:5
ru:132
sw:176
ta:21
te:68
th:34
tl:20
tpi:1088
tr:11
ur:60
vi:84
zh:295
$
```

# Miscellaneous
Here is the DDL for the ISO mapping data:
```sql
CREATE TABLE [ISO_639-3] (
         Id      char(3) NOT NULL,  -- The three-letter 639-3 identifier
         Part2B  char(3) NULL,      -- Equivalent 639-2 identifier of the bibliographic applications 
                                    -- code set, if there is one
         Part2T  char(3) NULL,      -- Equivalent 639-2 identifier of the terminology applications code 
                                    -- set, if there is one
         Part1   char(2) NULL,      -- Equivalent 639-1 identifier, if there is one    
         Scope   char(1) NOT NULL,  -- I(ndividual), M(acrolanguage), S(pecial)
         Type    char(1) NOT NULL,  -- A(ncient), C(onstructed),  
                                    -- E(xtinct), H(istorical), L(iving), S(pecial)
         Ref_Name   varchar(150) NOT NULL,   -- Reference language name 
         Comment    varchar(150) NULL)       -- Comment relating to one or more of the columns   
```

# Data Quality
For every gateway language called out by a language, this checks to see it is really is a gateway language based on the gateway flag for the language.

The query below returns all languages that are referenced as a gateway language but are not actually gateway languages. As of this writing there are 31 such invalid gateway languages.

```sql
select id,code,name,gateway_flag
from uw_language 
where id in (
	select gateway_language_id 
	from uw_language 
	where gateway_language_id is not null
)
and gateway_flag = false
order by code
```