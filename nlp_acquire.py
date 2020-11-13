import pandas as pd
import numpy as np
from requests import get
import os
from bs4 import BeautifulSoup

# Helper function that requests and parses HTML returning soup object.

def make_soup(url):
    '''
    This helper function takes in a url and requests and parses HTML
    returning a soup object.
    '''
    headers = {'User-Agent': 'Codeup Data Science'} 
    response = get(url, headers=headers)    
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Helper function that scrapes the blog urls from the main codeup blog page.

def get_all_urls():
    '''
    This function scrapes all of the Codeup blog urls from
    the main Codeup blog page and returns a list of urls.
    '''
    # The base url for the main Codeup blog page
    url = 'https://codeup.com/resources/#blog'
    
    # Make request and soup object using helper
    soup = make_soup(url)
    
    # Create a list of the anchor elements that hold the urls.
    urls_list = soup.find_all('a', class_='jet-listing-dynamic-link__link')
    
    # I'm using a set comprehension to return only unique urls because list contains duplicate urls.
    urls = {link.get('href') for link in urls_list}

    # I'm converting my set to a list of urls.
    urls = list(urls)
        
    return urls

# Function to create a DataFrame of article, title, and content and write to a json file.

def get_blog_articles(urls, cached=False):
    '''
    This function takes in a list of Codeup Blog urls and a parameter
    with default cached == False which scrapes the title and text for each url, 
    creates a list of dictionaries with the title and text for each blog, 
    converts list to df, and returns df.
    If cached == True, the function returns a df from a json file.
    '''
    if cached == True:
        df = pd.read_json('big_blogs.json')
        
    # cached == False completes a fresh scrape for df     
    else:

        # Create an empty list to hold dictionaries
        articles = []

        # Loop through each url in our list of urls
        for url in urls:

            # Make request and soup object using helper
            soup = make_soup(url)

            # Save the title of each blog in variable title
            title = soup.find('h1').text

            # Save the text in each blog to variable text
            content = soup.find('div', class_="jupiterx-post-content").text

            # Create a dictionary holding the title and content for each blog
            article = {'title': title, 'content': content}

            # Add each dictionary to the articles list of dictionaries
            articles.append(article)
            
        # convert our list of dictionaries to a df
        df = pd.DataFrame(articles)

        # Write df to a json file for faster access
        df.to_json('big_blogs.json')
    
    return df

def get_news_articles(cached=False):
    '''
    This function with default cached == False does a fresh scrape of inshort pages with topics 
    business, sports, technology, and entertainment and writes the returned df to a json file.
    cached == True returns a df read in from a json file.
    '''
    # option to read in a json file instead of scrape for df
    if cached == True:
        df = pd.read_json('articles.json')
        
    # cached == False completes a fresh scrape for df    
    else:
    
        # Set base_url that will be used in get request
        base_url = 'https://inshorts.com/en/read/'
        
        # List of topics to scrape
        topics = ['business', 'sports', 'technology', 'entertainment']
        
        # Create an empty list, articles, to hold our dictionaries
        articles = []

        for topic in topics:
            
            # Create url with topic endpoint
            topic_url = base_url + topic
            
            # Make request and soup object using helper
            soup = make_soup(topic_url)

            # Scrape a ResultSet of all the news cards on the page
            cards = soup.find_all('div', class_='news-card')

            # Loop through each news card on the page and get what we want
            for card in cards:
                title = card.find('span', itemprop='headline' ).text
                author = card.find('span', class_='author').text
                content = card.find('div', itemprop='articleBody').text

                # Create a dictionary, article, for each news card
                article = ({'topic': topic, 
                            'title': title, 
                            'author': author, 
                            'content': content})

                # Add the dictionary, article, to our list of dictionaries, articles.
                articles.append(article)
            
        # Create a DataFrame from list of dictionaries
        df = pd.DataFrame(articles)
        
        # Write df to json file for future use
        df.to_json('articles.json')
    
    return df