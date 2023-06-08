import util
import pandas as pd


def get_data(obj):
	df = pd.DataFrame.from_dict(obj)
	results = df["results"]
	urls, titles, dates = [], [], [] 
	
	for result in results:
		urls.append(result["url"])
		titles.append(result["title"])
		dates.append(result["created_date"])

	data = {
	'Headlines': titles,
	'Article Link': urls,
	'Date Published': dates
	}

	return pd.DataFrame(data)

def clean_dataframe(df):
    df = df.drop_duplicates(subset=None, keep="first", inplace=False)
    df = df.reset_index(drop=True)
    df['Date Published'] = pd.to_datetime(df['Date Published']).dt.strftime('%Y/%m/%d')
    return df

def main():
    # Obtain the URL required to make the API call
    url = util.get_config_details("NYT")
    
    # Make API call with three retry
    response = util.make_request(url,3,1)
    if not response:
        print("Please check URL!")
        return

    # Extract the required data
    output = get_data(response.json())
    if output.empty:
        print("No Data has been scraped")
        return None
    output = clean_dataframe(output)
   
    # Save the extracted data to csv
    util.save_data_to_csv(output, "Output/NYT.csv")

if __name__ == "__main__":
    main()