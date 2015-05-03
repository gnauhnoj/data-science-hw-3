import random
from helpers import reservoir_sample, loadAsNP, buildMovieDictionary
from file_helpers import getInfo, getMovies, getRatings

TRAIN_TEST_SPLIT = 0.7
USER_CUT = 0.5
ITEM_CUT = 0.4


def split_train_test_pointwise(data, len_items):
    """
    Randomly splits the data provided by the iterator data based on the TRAIN_TEST_SPLIT percentage
    the percentage corresponds to the percentage of the  dataset which should be allocated to training
    The split is performed on a per-rating level
    """
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
    return [iter(train), iter(test)]


def split_train_test_axiswise(data, len_users, len_items):
    """
    Randomly splits the data provided by the iterator data based on the USER_CUT and ITEM_CUT global variables
    these correspond to the percent of users and items which should be allocated into test dataset which should be allocated to training
    The split is performed on the intersection between selected users/items and doesn't correspond to an exact percentage split of reviews
    """
    remove_users = reservoir_sample(xrange(len_users), int(len_users * USER_CUT))
    remove_items = reservoir_sample(xrange(len_items), int(len_items * ITEM_CUT))
    train = []
    test = []
    for item in iter(data):
        if item[0] in remove_users and item[1] in remove_items:
            test.append(item)
        else:
            train.append(item)
    return [iter(train), iter(test), iter(remove_users), iter(remove_items)]


def get_train_data(axis_sample=True):
    """
    Retrieve and split the dataset into test / train
    Returns an output that is [training set as NP array, test review iterator, test user iterator, test movie iterator]
    """
    (users, items, reviews) = getInfo()
    data_generator = getRatings()
    if axis_sample:
        out = split_train_test_axiswise(data_generator, users, items)
    else:
        out = split_train_test_pointwise(data_generator, reviews)
    out[0] = loadAsNP(out[0], users, items)
    return out


def get_all_data():
    (users, items, reviews) = getInfo()
    data_generator = getRatings()
    return loadAsNP(data_generator, users, items)


def loadReccFile(recFileName):
    """
    Load reccomendation file and build NP array out of it
    returns NP array for checking complete predicted ratings
    """
    (users, items, reviews) = getInfo()
    data_generator = getRatings(recFileName)
    out = loadAsNP(data_generator, users, items, rebuild=True)
    return out
