import os
import sys

DATA_PATH = os.path.join(os.getcwd(), 'data')
ITEM_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.item')
DATA_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.data')
INFO_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.info')


# load as dictionary-generator
def getRatings(data_file=None):
    try:
        f = open(data_file, 'r')
    except:
        f = open(DATA_FILENAME, 'r')
    for l in f:
        (user_id, movie_id, rating, ts) = l.strip().split("\t")
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
        (id, movie) = l.strip().split('|')[0:2]
        id = int(id)
        yield (id, movie)
    f.close()
