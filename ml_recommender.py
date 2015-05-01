from movie_recommender import collaborative_filtering
from parse_movies.py import get_train_data

if __name__ == '__main__':
	train_data = get_train_data()
	cf = collaborative_filtering(train_data)
    cf.train()
    # get test data