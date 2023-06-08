import configparser
import time
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, urljoin
import csv
import json

# Obtain the details required to make the API call
def get_config_details(INFO):
    config = configparser.RawConfigParser()   
    config.read('configFile.ini')
    return config.get('URL_INFO', INFO)

# Make API call with three retry
def make_request(url,max_retries,retry_delay):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except RequestException as error:
            print(f" Error Occured : {error}")
            print(f" Retry Again --- retry count {retries}")
            retries+=1
            time.sleep(retry_delay)
        print(f"Request failed after {max_retries} retries")
        return None

# Save the extracted data to csv
def save_data_to_csv(df,csv_file_path):
    df.to_csv(csv_file_path, sep=',', encoding='utf-8')
    return None

