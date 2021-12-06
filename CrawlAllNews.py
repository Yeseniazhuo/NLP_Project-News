from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import requests
import random
import pandas as pd

def GetLoadedPageContent(url, n):
    '''
    Load all the news.
    :param url(str): The website url
           n(int): Click Times
    :return: html(str) the website's content after click more
    '''
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # open the page
    driver.get(url)
    # click the'More Articles' button by n times to load all the news
    for i in range(0, n):
        on_click = driver.find_element_by_class_name("load-more")
        ActionChains(driver).click(on_click).perform()
        time.sleep(3)  # wait for loading
        print('loading ----' + str(i))
    # Save loaded page content
    html = driver.page_source
    # Close the page
    driver.close()
    return html


def GetAllNewsUrl(Text):
    '''
    Get all the news' herf
    :param Text: url content
    :return: All news' link
    '''
    soup = BeautifulSoup(Text, 'lxml')
    body = soup.body
    # Find the content in the More news section
    MoreNews = body.find_all('a', {'class': 'stream-item__title'})
    News = [news['href'] for news in MoreNews]  # add all the herf to the News list
    # Get the news' href at Top part of the page
    HeadNews = body.find('h2', {'class': 'card--large__title'})
    SideNews = body.find_all('div', {'class': 'card card--small'})
    BottomNews = body.find_all('div', {'class': 'card__text'})
    # Get all the href in the top news
    TopNews = [HeadNews] + SideNews + BottomNews
    TopNews = [news.find('a') for news in TopNews]  # add all the herf to the News list
    TopNews = [news['href'] for news in TopNews]
    News = TopNews + News  # append the side news to the list
    #save all the news link to excel
    News_df = pd.DataFrame(columns=['url'], data=News)
    News_df.to_excel('NewsUrl.xlsx', index=False)
    return News


def GetNewsContext(url):
    '''
    Get the content of News's url
    :param: url(int): news series
    :return: Article(str):Article Content
    '''
    Response = requests.get(url)
    while (Response.status_code != 200):
        time.sleep(random.randint(15,30))
    Text = Response.text
    soup = BeautifulSoup(Text, 'lxml')
    # Get all the str in <p>
    Paragraphs = soup.find_all('p')
    Content = [Para.text for Para in Paragraphs]
    Article = '\n\n'.join(Content)
    return Article

def SaveNewsContext(News):
    '''
    :param News(List): News'urls list
    :return: null
    '''
    for i in range(0,len(News)):
        # Get the Article content
        Article = GetNewsContext(News[i])
        # Save all the file in Newsi.txt
        Name = News[i].split('/')
        if 'video' not in Name:
            TxtFileName = 'News/' + Name[-2] + '.txt'
            with open(TxtFileName, 'w') as file:
                file.write(Article)
            print('File '+str(i+1) + ' Download Successfully!')
            time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    # Parameters the current output base on date=23/11/2021
    n = 20  # click by 20 times
    url = 'https://www.forbes.com/business/'
    # Load the html after being clicked by 20 times
    Text = GetLoadedPageContent(url, n)
    # Analyze the html to get link
    News = GetAllNewsUrl(Text)
    # Get all the News Content and save in the .txt file
    SaveNewsContext(News)
