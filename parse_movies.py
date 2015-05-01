import sys
import os
import numpy as np
import random
# import math
# import time
# import json

DATA_PATH = os.path.join(os.getcwd(), 'data')
ITEM_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.item')
DATA_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.data')
INFO_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.info')
TRAIN_TEST_SPLIT = 0.8


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


def buildMovieDictionary(movie_generator):
    movies = {}
    for movie in movie_generator:
        (movie_id, movie_title) = movie
        movies[movie_id] = movie_title
    return movies


def buildRatingDictionary(data_generator, movie_generator=None):
    if movie_generator is not None:
        movies = buildMovieDictionary(movie_generator)
    ratings = {}
    for review in data_generator:
        (user_id, movie_id, rating) = review
        ratings.setdefault(user_id, {})
        if movie_generator is not None:
            ratings[user_id][(movie_id, movies[movie_id])] = rating
        else:
            ratings[user_id][movie_id] = rating
    return ratings


def loadAsNP(data_generator, users, items):
    matrix = np.zeros((users + 1, items + 1), dtype=float)
    for review in data_generator:
        (user_id, movie_id, rating) = review
        matrix[user_id][movie_id] = rating
    for movie_id in xrange(1, matrix.shape[1]):
        ratingNum = 0
        ratingSum = 0.0
        for user_id in xrange(1, matrix.shape[0]):
            if matrix[user_id][movie_id]:
                ratingNum += 1
                ratingSum += matrix[user_id][movie_id]
        if ratingNum > 0:
            matrix[0][movie_id] = ratingSum/ratingNum
    for user_id in xrange(1, matrix.shape[0]):
        ratingNum = 0
        ratingSum = 0.0
        for movie_id in xrange(1, matrix.shape[1]):
            if matrix[user_id][movie_id]:
                ratingNum += 1
                ratingSum += matrix[user_id][movie_id]
        if ratingNum > 0:
            matrix[user_id][0] = ratingSum/ratingNum
    return matrix


def get_rating(matrix, user_id, item_id):
    return matrix[user_id][item_id]


def split_train_test(data, len_items):
    split_index = int(len_items * TRAIN_TEST_SPLIT)
    iterator = iter(data)
    train = [next(iterator) for _ in range(split_index)]
    test = []
    n = split_index
    for item in iterator:
        n += 1
        s = random.randint(0, n)
        if s < split_index:
            test.append(train[s])
            train[s] = item
    return (iter(train), iter(test))


def get_train_data():
    (users, items, reviews) = getInfo()
    data_generator = getRatings()
    train = split_train_test(data_generator, reviews)[0]
    return loadAsNP(train, users, items)

if __name__ == '__main__':
    movie_generator = getMovies()
    data_generator = getRatings()
    (users, items, reviews) = getInfo()
    # ratings = buildRatingDictionary(movie_generator, data_generator)
    movies = buildMovieDictionary(movie_generator)
    train, test = split_train_test(data_generator, reviews)
    np_arr = loadAsNP(train, users, items)
