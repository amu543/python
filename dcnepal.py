import json
import requests 
from bs4 import BeautifulSoup 
from datetime import datetime 
# Target URL 
url = 'https://english.dcnepal.com/' 
# Fetch the page 
response = requests.get(url) 
soup = BeautifulSoup(response.text, features='html.parser') 

# Inside ul having class trending-topics-list, all li elements having a t
trending_news = soup.find_all('div', class_='thumbnail-news') 
print(trending_news)
articles_url=[]

for each_update in trending_news: 
    content= each_update.find('h3') 
    if content:
        url= content.find('a')['href']
        articles_url.append(url)


    
# print("Trending Articles URLs:", trending_articles_urls) 
# Visit trending articles and extract title, author, date and content 
articles_data = [] 
for each_article_url in articles_url: 
    article_response = requests.get(each_article_url) 
    article_soup = BeautifulSoup(article_response.text, features='html.parser') 
    title = article_soup.find('section', class_='single__content uk-margin-medium-top').find('h1').get_text(strip=True)
    content_paragraphs = article_soup.find('div', class_='news__wrap uk-margin-small-top').find_all('p')
    
    content = '\n'.join(p.get_text(strip=True) for p in content_paragraphs)
    articles_data.append({ 
        'title': title, 
        'content': content, 
        'url': each_article_url, 
        'scraped_at': datetime.now().isoformat() 
    }) 
print(articles_data)

filename="dcnepal.txt"
with open(filename, "w") as f:
    json.dump(articles_data, f, indent=4)
