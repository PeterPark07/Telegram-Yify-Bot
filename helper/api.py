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
    content = soup.find('div', class_='row')

    titles = content.find_all('div', class_='browse-movie-title')
    photos = content.find_all('img')
    ratings = content.find_all('span', class_='score font-meta total_votes')
    chapters = content.find_all('div', class_='list-chapter')

    results = []

    for title, photo, rating, chapter in zip(titles, photos, ratings, chapters):
        result = {}
        a_tag = title.find('a')
        if a_tag:
            result['title'] = a_tag.text.strip()
            result['link'] = a_tag['href']

        result['img'] = photo['data-src']
        result['rating'] = rating.text.strip()

        first_chapter = chapter.find('div', class_='chapter-item')
        if first_chapter:
            result['chapter'] = first_chapter.find('span', class_='chapter font-meta').text.strip()
            result['chapter_url'] = first_chapter.find('a', class_='btn-link')['href']

        results.append(result)
    return results
