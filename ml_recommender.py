from movie_recommender import collaborative_filtering
from parse_movies import get_train_data, get_all_data
from parse_movies import loadReccFile


def train_and_test():
	"""
	Loads the training for the movie_recommender
	Prints the RMSE value for the test data
	"""
	train_data, test_data, test_users, test_movies = get_train_data()
	print "loaded train & test data"
	cf = collaborative_filtering(train_data)
	# evaluate the collaborative filtering model by printing the rmse value for the test data
	print cf.score(test_data)


def write_reco(reco,user_id):
    recommendation_file = open('recommendation', 'a')
    recommendation_file.write( str(user_id) + '\t' + '\t'.join(map(str, reco)) + '\n')
    recommendation_file.flush()
    recommendation_file.close()


def get_recommendations(users_to_recommend):
	"""
	Print the recommendations for given set of users
	"""
	data = get_all_data()
	print "loaded data"
	precomputed_predictions = loadReccFile('ratings')
	print "loaded precomputed predictions"
	cf = collaborative_filtering(data, precomputed_predictions)
	print "initialized collaborative filter model"
	for user_id in users_to_recommend:
		recommendation = cf.recommendation(user_id)
		print "Recommendations for user : " + str(user_id)
		print [recc[0] for recc in recommendation]

if __name__ == '__main__':
	# users must be < 944
	users_to_recommend = [8, 900, 1, 35, 40]
	get_recommendations(users_to_recommend)
