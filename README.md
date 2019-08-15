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
    ```
    - using DBeaver, the result set is exported as JSON. Exporting notes:
        - Toggle off the setting `Print table name`
        - Use encoding UTF-8
        - Toggle off setting to "Insert BOM"
- `bin/dataprep.py`: this Python3 script will output:
    - one folder per language (in `data/languages`)
    - each folder will have:
        - the original JSON from `langnames.json` with the addition of a key named "gwcode" and its value. This will be the Gateway Language (if any) for the language.
        - the JSON converted to YAML format

During development there is debug code which restricts actions to 
only a few languages. This is avoid creation of 8K+ directories.

