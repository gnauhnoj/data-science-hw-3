from movie_recommender import collaborative_filtering
from parse_movies import get_train_data, get_all_data

def train_and_test():
	train_data, test_data, test_users, test_movies = get_train_data()
	print "loaded data"
	cf = collaborative_filtering(train_data)
	# cf.precompute_item_similarity()
	print cf.predict(1,3)
	print "Evaluating"
	print cf.score(test_data)
	# print cf.predict(1,3)
	# cf.train()
	# get test data


def write_reco(reco,user_id):
    recommendation_file = open('recommendation', 'a')
    recommendation_file.write( str(user_id) + '\t' + '\t'.join(map(str, reco)) + '\n')
    recommendation_file.flush()
    recommendation_file.close()

if __name__ == '__main__':
	# TODO: move get data to cf itself
	data = get_all_data()
	print "loaded data"
	cf = collaborative_filtering(data)
	print "initialized filter"
	for user_id in range(1,len(data)):
		recommendation = cf.recommendation(user_id)
		write_reco(recommendation,user_id)