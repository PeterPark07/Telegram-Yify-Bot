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

        image_url = image['src']
        if not image_url.startswith('http'):
            image_url = 'https://img.yts.mx' + image_url
        result['image'] = image_url
        
        result['year'] = year.text.strip()
        data = hid.text.strip().split()
        result['rating'] = data[0]
        result['genre'] = ' '.join(data[3:-2]).strip()

        results.append(result)
    return results

def movie(url):
    soup = get_soup(url)
    cover = soup.find('img', class_='img-responsive')['src']
    info = soup.find('div', class_='visible-xs col-xs-20').text.strip()
    tags = soup.find_all('div', class_='row')[6].text.strip()
    summary =  soup.find_all('div', class_='col-sm-10 col-md-13 col-lg-12')[0].text

    
    torrents = 'MAGNET LINKS - \n'
    for torrent in soup.find_all('div', class_='modal-torrent'):
        quality = torrent.find('div', class_='modal-quality').span.text
        size_elements = torrent.find_all('p', class_='quality-size')
        size = size_elements[1].text
        quality += ' ' + size_elements[0].text
    
        magnet_link = torrent.find('a', class_='magnet-download')['href']
        torrent = f"{quality}\n{size}\n{magnet_link}\n\n\n"
        torrents+=torrent

    similars = []
    for i in soup.find('div', class_='col-md-6 hidden-xs hidden-sm').find_all('a'):
        img = i.find('img')
        similars.append({'url': i['href'], 'title': i['title'], 'img': img['src']})


    return cover, info, tags, torrents, summary, similars
