import requests
from bs4 import BeautifulSoup
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}
def get_soup(url):
    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def get_movies(n):
    if n == 1:
        url = 'https://yts.mx/browse-movies/0/all/all/0/featured/0/all'
    elif n == 'trending':
        url = 'https://yts.mx/trending-movies'
    elif isinstance(n, int) :
        url = f'https://yts.mx/browse-movies/0/all/all/0/featured/0/all?page={n}'
    else:
        url = f'https://yts.mx/browse-movies/{n}'
        
    soup = get_soup(url)
    content = soup

    titles = content.find_all('a', class_='browse-movie-title')
    images = content.find_all('img', class_='img-responsive')
    years = content.find_all('div', class_='browse-movie-year')
    hidden = content.find_all('figcaption', class_='hidden-xs hidden-sm')
    
    results = []

    for title, image, year, hid in zip(titles, images, years, hidden):
        result = {}
        
        result['title'] = title.text.strip()
        result['url'] = title['href']
        
        if not image['src'].startswith('http'):
            result['image'] = 'https://img.yts.mx' + image['src']
        
        result['year'] = year.text.strip()
        data = hid.text.strip().split()
        result['rating'] = data[0]
        result['genre'] = ' '.join(data[3:-2]).strip()

        results.append(result)
    return results

