from movie_recommender import collaborative_filtering
from parse_movies import get_train_data

if __name__ == '__main__':
	# TODO: move get data to cf itself
	train_data = get_train_data()
	# print len(train_data[0])
	cf = collaborative_filtering(train_data)
	cf.precompute_item_similarity()
	# cf.train()
	# get test data