import util
from bs4 import BeautifulSoup
import pandas as pd

def get_bbc_title(article_url):
    #Parse the webpage and get article and title of the target URL
    base_url = f'https://www.bbc.com{article_url}'
    res = util.make_request(base_url,3,1)
    if res:
        soup = BeautifulSoup(res.content, "html.parser")

    #Parse time attribute to get publish time field
    #Loop breaks after getting hold of the  first instance - to avoid iteration over all time attributes
        for i in soup.findAll('time'):
            if i.has_attr('datetime'):
                dateVar = i['datetime']
                break
    #Parse and get the title of the article
        if soup.find('h1',id ='main-heading'):
            title = soup.find('h1',id ='main-heading').text
            result = [title,dateVar]
            return result
    else:
        return None


def scrape_bbc(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    urls, titles, dates = [], [], []
    #Getting all the valid urls from a tag
    for link in soup("a", "gs-c-promo-heading", href=True):
        article_url = link['href']

        #For each url - need to visit the article page to get tiltle and date
        #'''Certain urls are outside bbc.news domain - we skip those urls 
        #   for the scope of this assessment as the target webpage layout differs'''
        if 'www.bbc.com' not in article_url:
            data = get_bbc_title(article_url)    
            if data:
                urls.append(f'https://www.bbc.com{article_url}')
                titles.append(data[0])
                dates.append(data[1])
            else:
                continue
    
    data = {'Headlines': titles,
            'Article Link': urls,
            'Date_Published' : dates
            }

    return data

def convert_to_dataframe(data):
    if not data:
        print("No Data has been scraped")
        return None
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=None, keep="first", inplace=False)
    df = df.reset_index(drop=True)
    df['Date_Published'] = pd.to_datetime(df['Date_Published']).dt.strftime('%Y/%m/%d')
    return df

def main():
    #Get all configs
    url = util.get_config_details("BBC")

    # Make API call with three retry
    response = util.make_request(url,3,1)
    if not response:
        print("Please check URL!")
        return
        
    # Extract the required data
    data = scrape_bbc(response)
    dataframe = convert_to_dataframe(data)
    if dataframe.empty:
        print("DataFrame is Empty")
        return 
    
    # Save the extracted data to csv
    util.save_data_to_csv(dataframe, 'Output/BBC.csv')

if __name__ == "__main__":
    main()