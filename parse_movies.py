import sys
import os
import numpy as np
# import math
# import random
# import time
# import json

DATA_PATH = os.path.join(os.getcwd(), 'data')
ITEM_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.item')
DATA_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.data')
INFO_FILENAME = os.path.join(DATA_PATH, 'ml-100k/u.info')


# load as dictionary-generator
def parseFile(item_file=None, data_file=None):
    movies = {}
    try:
        f = open(item_file, 'r')
    except:
        f = open(ITEM_FILENAME, 'r')
    for l in f:
        (id, movie) = l.strip().split('|')[0:2]
        id = int(id)
        movies[id] = movie
    ratings = {}
    try:
        f = open(data_file, 'r')
    except:
        f = open(DATA_FILENAME, 'r')
    for l in f:
        (user_id, movie_id, rating, ts) = l.strip().split("\t")
        user_id = int(user_id)
        movie_id = int(movie_id)
        ratings.setdefault(user_id, {})
        ratings[user_id][(movie_id, movies[movie_id])] = float(rating)
    f.close()
    # return ratings
    for user in ratings:
        yield (user, ratings[user])


def getInfo(info_file=None):
    stats = []
    try:
        f = open(info_file, 'r')
    except:
        f = open(INFO_FILENAME, 'r')
    for l in f:
        stat = int(l.strip().split()[0])
        stats.append(stat)
    return stats


def loadAsNP(generator, users, items):
    matrix = np.zeros((users + 1, items + 1), dtype=float)
    for user in generator:
        user_id = user[0]
        for reviews in user[1]:
            movie_id = reviews[0]
            matrix[user_id][movie_id] = user[1][reviews]
    for movie_id in xrange(1, matrix.shape[1]):
        ratingNum = 0
        ratingSum = 0.0
        for user_id in xrange(1, matrix.shape[0]):
            if matrix[user_id][movie_id]:
                ratingNum += 1
                ratingSum += matrix[user_id][movie_id]
        matrix[0][movie_id] = ratingSum/ratingNum
    for user_id in xrange(1, matrix.shape[0]):
        ratingNum = 0
        ratingSum = 0.0
        for movie_id in xrange(1, matrix.shape[1]):
            if matrix[user_id][movie_id]:
                ratingNum += 1
                ratingSum += matrix[user_id][movie_id]
        matrix[user_id][0] = ratingSum/ratingNum
    return matrix


def get_rating(matri, user_id, item_id):
    return matrix[user_id][item_id]


if __name__ == '__main__':
    generator = parseFile()
    (users, items, reviews) = getInfo()
    np_arr = loadAsNP(generator, users, items)
