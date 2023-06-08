#In this module, we will be using BeautifulSoup and requests library to scrape the contents of Economist webpage
import util
import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import numpy as np
import re 

def scrape_news(response):
    urls, titles, dates = [], [], [] 
    soup = BeautifulSoup(response.content, "html.parser")
    # Get the content of web page - to get hold of selectors
    main_content = soup.find_all(role="main", id="content")
    
    for content in main_content:
        # Find all anchor tags within the content
        anchor_tags = content.find_all('a')
        
        # Iterate over the anchor tags and extract the URL, title, and date
        for anchor_tag in anchor_tags:
            # Extract URL
            url = anchor_tag['href']
            
            # Extract date from the URL
            parsed_url = urlparse(url)
            path_components = parsed_url.path.split('/')            
            date_published = "/".join(path_components[2:5])
            if date_published == "" or re.search('[a-zA-Z]', date_published):
                date_published = False
            
            # Extract accompanying title
            title = anchor_tag.text
            
            if title and date_published:
                urls.append(f'https://www.economist.com{url}')
                titles.append(title) 
                dates.append(date_published)
    data = {
        'Headlines': titles,
        'Article Link': urls,
        'Date Published': dates
        }
    
    return data

def convert_to_dataframe(data):
    if not data:
        print("No Data has been scraped")
        return None
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=None, keep="first", inplace=False)
    filter = df["Date Published"] != False
    df = df[filter]
    df['Date Published'] = df['Date Published'].replace(['-'],'/')
    df = df.reset_index(drop=True)
    return df

def main():
    #Get all configs
    url = util.get_config_details("ECONOMIST")

    # Make API call with three retry
    response = util.make_request(url,3,1)
    if not response:
        print("Please check URL!")
        return

    # Extract the required data
    output = scrape_news(response)
    dataframe = convert_to_dataframe(output)
    
    # Save the extracted data to csv
    if dataframe.empty:
        print("DataFrame is Empty")
        return  
    util.save_data_to_csv(dataframe, 'Output/Economist.csv')

if __name__ == "__main__":
    main()