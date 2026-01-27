import json
import requests 
from bs4 import BeautifulSoup 
from datetime import datetime 
# Target URL 
url = 'https://nepalitimes.com/' 
# Fetch the page 
response = requests.get(url) 
soup = BeautifulSoup(response.text, features='html.parser') 

# Inside ul having class trending-topics-list, all li elements having a t
latest_news = soup.find_all('article', class_='list') 
print(latest_news)
articles_url=[]

for each_update in latest_news: 
    parent_a = each_update.find_parent('a')
    each_update = parent_a['href']
    url= 'https://nepalitimes.com' + each_update
    articles_url.append(url)

    
# print("Trending Articles URLs:", trending_articles_urls) 
# Visit trending articles and extract title, author, date and content 
articles_data = [] 
for each_article_url in articles_url: 
    article_response = requests.get(each_article_url) 
    article_soup = BeautifulSoup(article_response.text, features='html.parser') 
    title = article_soup.find('article', class_='article__full').find('h1').get_text(strip=True)
    content_paragraphs = article_soup.find('div', class_='article__text').find_all('p')
    
    content = '\n'.join(p.get_text(strip=True) for p in content_paragraphs)
    articles_data.append({ 
        'title': title, 
        'content': content, 
        'url': each_article_url, 
        'scraped_at': datetime.now().isoformat() 
    }) 
print(articles_data)

filename="exem.txt"
with open(filename, "w") as f:
    json.dump(articles_data, f, indent=4)
