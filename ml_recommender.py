from movie_recommender import collaborative_filtering
from parse_movies import get_train_data

if __name__ == '__main__':
	# TODO: move get data to cf itself
	train_data, test_data, test_users, test_movies = get_train_data()
	print "loaded data"
	# print len(train_data[0])
	cf = collaborative_filtering(train_data)
	# cf.precompute_item_similarity()
	print cf.predict(1,3)
	print "Evaluating"
	print cf.score(test_data)
	# print cf.predict(1,3)
	# cf.train()
	# get test data