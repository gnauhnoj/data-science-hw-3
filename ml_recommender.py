from movie_recommender import collaborative_filtering
from parse_movies import get_train_data

if __name__ == '__main__':
	# TODO: move get data to cf itself
	train_data, test_data, test_users, test_movies = get_train_data()
	print "loaded data"
	total = 0.0
	count = 0.0
	for movie_id in range(1, train_data.shape[1]):
		for user_id in range(1, train_data.shape[0]):
			if train_data[user_id][movie_id]:
				total += train_data[user_id][movie_id]
				count += 1
	
	avg = (total/float(count)) if (count != 0) else 0.0
	print avg
	cf = collaborative_filtering(train_data,avg)
	# cf.precompute_item_similarity()
	print cf.predict(1,3)
	print "Evaluating"
	print cf.score(test_data)
	# print cf.predict(1,3)
	# cf.train()
	# get test data