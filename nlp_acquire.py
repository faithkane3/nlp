import pandas as pd
import numpy as np
from requests import get
import os
from bs4 import BeautifulSoup

def get_all_urls():
    '''
    This function scrapes all of the Codeup blog urls from
    the main Codeup blog page and returns a list of urls.
    '''
    # The main Codeup blog page with all the urls
    url = 'https://codeup.com/resources/#blog'
    
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    # Send request to main page and get response
    response = get(url, headers=headers)
    
    # Create soup object using response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Create empty list to hold the urls for all blogs
    urls = []
    
    # Create a list of the element tags that hold the href/links
    link_list = soup.find_all('a', class_='jet-listing-dynamic-link__link')
    
    # get the href/link from each element tag in my list
    for link in link_list:
        
        # Add the link to my urls list
        urls.append(link['href'])
        
    return urls


def get_blog_articles(urls, cache=False):
    '''
    This function takes in a list of Codeup Blog urls and a parameter
    with default cache == False which returns a df from a csv file.
    If cache == True, the function scrapes the title and text for each url, creates a list of dictionaries
    with the title and text for each blog, converts list to df, and returns df.
    '''

    if cache == False:
        df = pd.read_csv('big_blogs.csv', index_col=0)
    else:
        headers = {'User-Agent': 'Codeup Data Science'} 

        # Create an empty list to hold dictionaries
        articles = []

        # Loop through each url in our list of urls
        for url in urls:

            # get request to each url saved in response
            response = get(url, headers=headers)

            # Create soup object from response text and parse
            soup = BeautifulSoup(response.text, 'html.parser')

            # Save the title of each blog in variable title
            title = soup.find('h1', itemprop='headline' ).text

            # Save the text in each blog to variable text
            text = soup.find('div', itemprop='text').text

            # Create a dictionary holding the title and text for each blog
            article = {'title': title, 'content': text}

            # Add each dictionary to the articles list of dictionaries
            articles.append(article)
        # convert our list of dictionaries to a df
        df = pd.DataFrame(articles)

        # Write df to csv file for faster access
        df.to_csv('big_blogs.csv')
    
    return df


def get_news_articles(cache=False):
    '''
    This function uses a cache parameter with default cache == False to give the option of 
    returning in a df of inshorts topics and info by reading a csv file or
    of doing a fresh scrape of inshort pages with topics business, sports, technology,
    and entertainment and writing the returned df to a csv file.
    '''
    # default to read in a csv instead of scrape for df
    if cache == False:
        df = pd.read_csv('articles.csv', index_col=0)
        
    # cache == True completes a fresh scrape for df    
    else:
    
        # Set base_url and headers that will be used in get request

        base_url = 'https://inshorts.com/en/read/'
        headers = {'User-Agent': 'Codeup Data Science'}

        # List of topics to scrape
        topics = ['business', 'sports', 'technology', 'entertainment']

        # Create an empty list, articles, to hold our dictionaries
        articles = []

        for topic in topics:

            # Get a response object from the main inshorts page
            response = get(base_url + topic, headers=headers)

            # Create soup object using response from inshort
            soup = BeautifulSoup(response.text, 'html.parser')

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
            
        # Why not return it as a DataFrame?!
        df = pd.DataFrame(articles)
        
        # Write df to csv for future use
        df.to_csv('articles.csv')
    
    return df