import random
from helpers import reservoir_sample, loadAsNP, buildMovieDictionary
from file_helpers import getInfo, getMovies, getRatings

TRAIN_TEST_SPLIT = 0.7
USER_CUT = 0.4
ITEM_CUT = 0.7


def split_train_test_pointwise(data, len_items):
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


def split_train_test_axiswise(data, len_users, len_items):
    remove_users = reservoir_sample(xrange(len_users), int(len_users * USER_CUT))
    remove_items = reservoir_sample(xrange(len_items), int(len_items * ITEM_CUT))
    train = []
    test = []
    for item in iter(data):
        if item[0] in remove_users and item[1] in remove_items:
            test.append(item)
        else:
            train.append(item)
    return (iter(train), iter(test), iter(remove_users), iter(remove_items))


def get_train_data():
    (users, items, reviews) = getInfo()
    data_generator = getRatings()
    train = split_train_test(data_generator, reviews)[0]
    return loadAsNP(train, users, items)


if __name__ == '__main__':
    movie_generator = getMovies()
    (users, items, reviews) = getInfo()
    movies = buildMovieDictionary(movie_generator)
    data_generator = getRatings()
    # train, test = split_train_test_pointwise(data_generator, reviews)
    train, test = split_train_test_axiswise(data_generator, users, items)[0:2]
