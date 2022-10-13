#!/usr/bin/env python3
# coding: utf-8


import requests
import csv
import os

OUTPUT_DIR = "extract_matomo"
OUTPUT_FILE = "page_editors_traffic_matomo.csv"
URL_API = "https://opendatasoft.matomo.cloud/index.php?module=API&format=json&idSite=7&period=day&date=last5&method=CustomReports.getCustomReport&reportUniqueId=CustomReports_getCustomReport_idCustomReport--21&filter_limit=-1&format_metrics=1&expanded=1"
QUERY_STUDIO = '&idCustomReport=21'
QUERY_CODE_EDITOR = '&idCustomReport=24'
HEADERS = {'token_auth': os.environ.get('matomo_token', '{{ pillar.apikeys.matomo|trim }}')}

#function to get the data using matomo api
def get_data(query):
    url = URL_API + query
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def main():
  #get data from both studio and code editor dashboards
  studio = get_data(QUERY_STUDIO)
  code_editor= get_data(QUERY_CODE_EDITOR)
 
  #turn both dict into lists and zip it all
  big_table = zip(list(studio.keys()),list(studio.values()),list(code_editor.values()))
  
  #append the csv file with the 5 last days
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  with open(os.path.join(OUTPUT_DIR, OUTPUT_FILE), "a") as out:
    writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for row in big_table:
        writer.writerow(row)
      
if __name__ == "__main__":
    main()
