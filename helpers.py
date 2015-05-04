import random
import numpy as np


def reservoir_sample(iterator, k):
    """
    Basic reservoir sample. Takes a target sample amount
    """
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
    """
    Retrieve a rating for a user given a rating matrix, userid, and itemid
    """
    return matrix[user_id][item_id]


def loadAsNP(data_generator, users, items, rebuild=False):
    """
    Returns an NP array which contains all ratings as provided by the data generator
    Requires total users and total items to be passed in (in order to create the array)
    Rebuild variable indicates whether this is being used to rebuild predicted rating table -- if so, it will also return a map of user reviews in the format map[userid][movieid]
    """
    matrix = np.zeros((users + 1, items + 1), dtype=float)
    contribMap = {}
    for review in data_generator:
        (user_id, movie_id, rating, ts) = review
        matrix[user_id][movie_id] = rating
        if ts == 0 and rebuild:
            contribMap.setdefault(user_id, {})
            contribMap[user_id][movie_id] = 1
    for movie_id in xrange(1, matrix.shape[1]):
        ratingNum = 0
        ratingSum = 0.0
        for user_id in xrange(1, matrix.shape[0]):
            if matrix[user_id][movie_id]:
                ratingNum += 1
                ratingSum += matrix[user_id][movie_id]
        if ratingNum:
            matrix[0][movie_id] = ratingSum/ratingNum
    totalNum = 0
    totalSum = 0.0
    for user_id in xrange(1, matrix.shape[0]):
        ratingNum = 0
        ratingSum = 0.0
        for movie_id in xrange(1, matrix.shape[1]):
            if matrix[user_id][movie_id]:
                ratingNum += 1
                ratingSum += matrix[user_id][movie_id]
                totalNum += 1
                totalSum += matrix[user_id][movie_id]
        if ratingNum:
            matrix[user_id][0] = ratingSum/ratingNum
    if totalSum:
        matrix[0][0] = totalSum/totalNum
    if rebuild:
        return (matrix, contribMap)
    return matrix


def buildMovieDictionary(movie_generator):
    """
    Build Movie Dictionary from Movie Generator
    Movie Dictionary maps movie id to (title, genre list)
    """
    movies = {}
    for movie in movie_generator:
        (movie_id, movie_title, genres) = movie
        movies[movie_id] = (movie_title, genres)
    return movies


def buildRatingDictionary(data_generator, movie_generator=None):
    """
    Build rating dictionary from data generator if movie_generator is passed it will return movie id and title as movie key
    IF not - it returns a dictionary mapping dic[userid][movieid] = rating
    """
    if movie_generator is not None:
        movies = buildMovieDictionary(movie_generator)
    ratings = {}
    for review in data_generator:
        (user_id, movie_id, rating) = review[0:3]
        ratings.setdefault(user_id, {})
        if movie_generator is not None:
            ratings[user_id][(movie_id, movies[movie_id])] = rating
        else:
            ratings[user_id][movie_id] = rating
    return ratings


def getDiverseRecc(sortedRecs, movieMap, userMap, user_id):
    """
    Function which generates reccomendations based on a sorted list of predicted values
    Returns top 5 non-rated movies and 5 "diverse" movies of different genres

    movieMap is a dictionary mapping movieid to movietitle and genre
    userMap is a dictionary mapping user rated movies as userMap[userid][movieid] = 0/1
    user_id is the user recomendations are being generated for
    """
    genreMap = {}
    out = []
    ptr = 0
    maxVal = 1
    count = 0
    while len(out) < 10:
        movie_id = sortedRecs[ptr]
        movie = movieMap[movie_id]
        try:
            userMap[user_id][movie_id]
            count += 1
        except KeyError:
            for genre in movie[1]:
                genreMap.setdefault(genre, 0)
                if genreMap[genre] < maxVal and movie not in out:
                    out.append(movie)
                    for genre2 in movie[1]:
                        genreMap.setdefault(genre2, 0)
                        genreMap[genre2] += 1
                    break
        if ptr == len(sortedRecs)-1:
            if (len(out) + count) == len(sortedRecs):
                break
            ptr = 0
            maxVal += 1
            count = 0
            continue
        ptr += 1
    return out
