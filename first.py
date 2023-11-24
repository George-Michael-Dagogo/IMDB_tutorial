#import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import concurrent.futures
from sqlalchemy import create_engine

titles = []
years = []
ratings = []
genres = []
runtimes = []
imdb_ratings = []
metascores = []
votes = []

url = [f'https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,&sort=release_date,asc&start={i:d}&ref_=adv_nxt' for i in (range(1,9000,50))]
def scraper(uri):

    page = requests.get(uri)

    soup = BeautifulSoup(page.text, 'html.parser')

    movie_box = soup.find_all('div', class_= "lister-item mode-advanced")


    for box in movie_box:
        #title
        if box.find('h3', class_ = 'lister-item-header') is not None:
            title = box.find('h3', class_ = 'lister-item-header').a.text
            titles.append(title)
        else:
            titles.append('None')

        #year released
        if box.h3.find('span', class_="lister-item-year text-muted unbold") is not None:
            year = box.h3.find('span', class_="lister-item-year text-muted unbold").text
            years.append(year)
        else:
            years.append('None')

        #ratings
        if box.p.find('span', class_= 'certificate') is not None:
            rating = box.p.find('span', class_= 'certificate').text
            ratings.append(rating)
        else:
            ratings.append('None')

        #genre
        if box.p.find('span', class_= 'genre') is not None:
            genre = box.p.find('span', class_= 'genre').text.replace('\n','').rstrip()
            genres.append(genre)
        else:
            genres.append('None')

        #runtimes
        if box.p.find('span', class_= 'runtime') is not None:
            runtime = int(box.p.find('span', class_= 'runtime').text.replace(' min',''))
            runtimes.append(runtime)
        else:
            runtimes.append('None')

        #imdb ratings inline-block ratings-imdb-rating
        if box.find('div', class_= 'inline-block ratings-imdb-rating') is not None:
            imdb_rating = float(box.find('div', class_= 'inline-block ratings-imdb-rating').text)
            imdb_ratings.append(imdb_rating)
        else:
            imdb_ratings.append('None')

        #metascores
        if box.find('span', class_= 'metascore') is not None:
            metascore = int(box.find('span', class_= 'metascore').text)
            metascores.append(metascore)
        else:
            metascores.append('None')

        #votes
        if box.find('p', class_= 'sort-num_votes-visible') is not None:
            vote = box.find('p', class_= 'sort-num_votes-visible').text.replace('\n','').replace('Votes:','').replace(',','')
            votes.append(vote)
        else:
            votes.append('None')
    print(uri)

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(scraper,url)

movie_df = pd.DataFrame({
    'movie':titles,
    'year':years,
    'rating':ratings,
    'genre':genres,
    'runtime_minutes': runtimes,
    'imdb_rating':imdb_ratings,
    'metascore':metascores,
    'votes':votes
})
movie_df['year'] = movie_df['year'].str[-5:-1]

movie_df.to_csv('movies.csv',index=False)


# conn_string = 'postgresql://testtech:Michael1234@testtech.postgres.database.azure.com:5432/postgres'
# db = create_engine(conn_string)
# conn = db.connect()
# movie_df.to_sql('movies',con = conn, if_exists='append', index = False)
print('pushed successfully')
