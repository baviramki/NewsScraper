# NewsScraper
NewsScraper Module in Python to extract headlines, url and publish date from different new websites

# **Problem Statements:**
Please choose a news site of your choice and build an automation that can provide the following 3 elements:
1. The headline of the articles on the main page.
2. The date each article was published.
3. A link to each article

# **Key Insights:**
For this evaluation, I have explored three different websites:
1. Economist.com
2. BBC.com
3. NewyorkTimes.com

Python offers several modules for web scraping, such as BeautifulSoup, Scrapy, and Selenium. In this project, I utilized BeautifulSoup for the automation process.

**economist.com:** This website possesses a straightforward structure that perfectly suits web automation. All selector tags have consistent names, making it easier to extract fields from articles on the main page.

**bbc.com:** This website has a distinct structure that requires additional processing and data validation after extracting the URL. Extracting the publication date posed a challenge as it required visiting the article page and retrieving the date parameter.

**nytimes.com:** The New York Times website features a dynamic webpage layout. The selectors are relatively dynamic compared to the previous websites, making it less suitable for screen scraping. However, automation can be achieved by utilizing the NYT API, which provides a more robust and standardized approach to obtaining all the required fields.

# **Install Dependencies:**
```
pip3 install requests
pip3 install pandas
pip3 install re
pip3 install beautifulsoup4
pip3 install configparser
pip3 install urllib3
```

# **To Run:**
1. To scrape economist.com
```python3 economist.py```

2. To scrape bbc.com
```python3 bbc.py```

3. To scrape nytimes.com
```python3 nyt.py```
