import random
import numpy as np


def reservoir_sample(iterator, k):
    # fill the reservoir to start
    iterator = iter(iterator)
    result = [next(iterator) for _ in range(k)]
    n = k
    for item in iterator:
        n += 1
        s = random.randint(0, n)
        if s < k:
            result[s] = item
    return result


def get_rating(matrix, user_id, item_id):
    return matrix[user_id][item_id]


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
