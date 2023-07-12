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

def trending():
    url = 'https://yts.mx/browse-movies/0/all/all/0/featured/0/all'
    soup = get_soup(url)
    content = soup

    titles = content.find_all('a', class_='browse-movie-title')
    images = content.find_all('img', class_='img-responsive')
    years = content.find_all('div', class_='browse-movie-year')
    ratings = content.find_all('h4', class_='rating')

    print(titles)
    print(images)
    print(years)
    print(ratings)

    
    results = []

    for title, image, year, rating in zip(titles, images, years, ratings):
        result = {}
        
        result['title'] = title.text.strip()
        result['url'] = title['href']
        result['image'] = image['src']
        result['year'] = year.text.strip()
        result['rating'] = rating.text.strip()

        results.append(result)
    return results
