from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import time

oldestYearLimit = 2020

def parseImdbPage(url, year, id):
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html.parser")
    moviesOnPage = {}
    movieElementList = soup.findAll('div', attrs={'class': 'lister-item-content'})

    
    for movieElement in movieElementList:
        movieEntry = {
			'name': '',
            'rating': '',
            'year': str(year),
            'certificate': '',
            'runtime': '',
            'genre': '',
            'description': '',
            # 'director': '',
            # 'stars': []
            # 'votes': '',
            # 'gross': ''
        }
        if movieElement.find('h3', attrs={'class': 'lister-item-header'}).find('a').text:
            nameValue = movieElement.find('h3', attrs={'class': 'lister-item-header'}).find('a').text.strip()
            movieEntry['name'] = nameValue
        if movieElement.find('div', attrs={'class': 'ratings-bar'}):
            if movieElement.find('div', attrs={'class': 'ratings-bar'}).find('strong').text:
                ratingValue = movieElement.find('div', attrs={'class': 'ratings-bar'}).find('strong').text.strip()
                movieEntry['rating'] = ratingValue
        
        p_list = movieElement.findAll('p')

        if p_list[0]:
            if p_list[0].find('span', attrs={'class': 'certificate'}):
                certificate_value = p_list[0].find('span', attrs={'class': 'certificate'}).text.strip()
                movieEntry['certificate'] = certificate_value

            if p_list[0].find('span', attrs={'class': 'runtime'}):
                runtime_value = p_list[0].find('span', attrs={'class': 'runtime'}).text.strip()
                movieEntry['runtime'] = runtime_value

            if p_list[0].find('span', attrs={'class': 'genre'}):
                genre_value = p_list[0].find('span', attrs={'class': 'genre'}).text.strip()
                movieEntry['genre'] = genre_value

        if p_list[1]:
            description_value = p_list[1].text.strip()
            movieEntry['description'] = description_value
        
        moviesOnPage[id] = movieEntry
        id += 1
    
    return moviesOnPage, id

def ParseImdb():
    currentYear = int(datetime.datetime.now().year)
    allMoviesDb = {}
    id = 0 # Ugly but this is how we do it
    for year in range(oldestYearLimit, currentYear + 1):
        url = "https://www.imdb.com/search/title/?release_date=" + str(year) + "," + str(year) + "&title_type=feature"
        newMovies, id = parseImdbPage(url, year, id)
        allMoviesDb = {**allMoviesDb, **newMovies}
        time.sleep(1)
        print("retrieved movies from " + str(year))
    return allMoviesDb
