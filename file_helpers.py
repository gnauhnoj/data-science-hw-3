import os
import sys

DATA_PATH = os.path.join(os.getcwd(), 'data')
ITEM_FILENAME_100k = os.path.join(DATA_PATH, 'ml-100k/u.item')
DATA_FILENAME_100k = os.path.join(DATA_PATH, 'ml-100k/u.data')
INFO_FILENAME_100k = os.path.join(DATA_PATH, 'ml-100k/u.info')
delim1_100k = '\t'
delim2_100k = '|'

ITEM_FILENAME_1M = os.path.join(DATA_PATH, 'ml-1m/movies.dat')
DATA_FILENAME_1M = os.path.join(DATA_PATH, 'ml-1m/ratings.dat')
INFO_FILENAME_1M = os.path.join(DATA_PATH, 'ml-1m/info.dat')
delim_1M = '::'

ITEM_FILENAME = ITEM_FILENAME_100k
DATA_FILENAME = DATA_FILENAME_100k
INFO_FILENAME = INFO_FILENAME_100k
delim1 =        delim1_100k
delim2 =        delim2_100k

genreMap = ['unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']


# load as dictionary-generator
def getRatings(data_file=None):
    try:
        f = open(data_file, 'r')
    except:
        f = open(DATA_FILENAME, 'r')
    for l in f:
        (user_id, movie_id, rating, ts) = l.strip().split(delim1)
        user_id = int(user_id)
        movie_id = int(movie_id)
        rating = float(rating)
        yield (user_id, movie_id, rating)
    f.close()


def getInfo(info_file=None):
    stats = []
    try:
        f = open(info_file, 'r')
    except:
        f = open(INFO_FILENAME, 'r')
    for l in f:
        stat = int(l.strip().split()[0])
        stats.append(stat)
    f.close()
    return stats


def getMovies(item_file=None):
    try:
        f = open(item_file, 'r')
    except:
        f = open(ITEM_FILENAME, 'r')
    for l in f:
        line = l.strip().split(delim2)
        (id, movie) = line[0:2]
        temp = [int(num) for num in line[5:24]]
        genres = []
        for i, genre in enumerate(temp):
            if genre == 1:
                genres.append(genreMap[i])
        id = int(id)
        yield (id, movie, genres)
    f.close()
