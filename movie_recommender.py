import numpy as np
from scipy.stats.stats import pearsonr
from operator import itemgetter
from sklearn.metrics import mean_squared_error
from math import sqrt
from helpers import buildMovieDictionary, getDiverseRecc
from file_helpers import getMovies
import warnings
warnings.filterwarnings("ignore")

class collaborative_filtering:
    def __init__(self, data, predictions = [0,0]):
        """
        Initialize the class instance with required data to build the model
        Receives 2D numpy array containing data about the ratings by each user for each movie id
        Rating is zero if the user has not rated the movie till now
        predictions is a tuple containing the precomputed data for recommendations and the user map
        """
        self.put_data(data, predictions)

    def get_data(self):
        return self.data


    def put_data(self,data, predictions):
        self.data = data
        self.n_movies = len(data[0])
        self.global_average = data[0][0]
        self.item_similarity = np.zeros((self.n_movies, self.n_movies), dtype=float)
        self.similarity_calculated = np.zeros(self.n_movies, dtype=float)
        self.predictions = predictions[0]
        self.user_map = predictions[1]
        self.movie_map = buildMovieDictionary(getMovies())
        return


    def similarity(self, item_1, item_2):
        """
        Method to compute similarity between 2 movie vectors
        Receives the rating vectors for 2 movies
        Returns the pearson similarity coefficient by considering only co-rated items
        """
        new_1 = []
        new_2 = []
        for i in range(1,len(item_1)):
            if (item_1[i] != 0) or (item_2[i] != 0):
                new_1.append(item_1[i])
                new_2.append(item_2[i])
        if (len(new_1) == 0) or (len(new_2) == 0):
            return 0.0
        similarity_value = pearsonr(new_1,new_2)[0]
        return similarity_value


    def get_similar_movies(self, item_1):
        """
        Find similar movies given a movie id
        """
        all_items = range(1,self.n_movies)
        movie_1 = self.data[:,item_1]
        # print movie_1
        if self.similarity_calculated[item_1] == 0:
            similarities = np.zeros(self.n_movies, dtype=float)
            for item_2 in all_items:
                movie_2 = self.data[:,item_2]
                if( (item_1 != item_2) or  (movie_1[0] != 0.0) or  (movie_2[0] != 0.0) ):
                    try:
                        similarities[item_2] = self.similarity(movie_1,movie_2)
                        self.item_similarity[item_1][item_2] = similarities[item_2]
                    except Exception as e:
                        print e
                        print item_1, item_2
        else:
            similarities = self.item_similarity[item_1]
        self.similarity_calculated[item_1] = 1
        return np.argsort(similarities),similarities


    def predict(self,user_id,movie_id):
        """
        Receives a user_id and a movie_id
        Returns the rating the user will give to the movie using combination of
        item based collaborative filtering and global baseline approach
        """
        # get similarity value of all other movies(items) for the given movie
        similar_movies, movies_similarity = self.get_similar_movies(movie_id)

        # get all the ratings posted by the user
        user_rating = self.data[user_id,:]
 
        # mean_user_rating = mean(user_rating)
        mean_user_rating = user_rating[0]
        # user_rating = self.center_rating(user_rating,mean_user_rating)

        prediction = 0.0
        total_sum = 0.0

        # do a weighted sum of users existing reviews after adjusting for baseline
        # weights are based on the similarity values
        for movie in similar_movies:
            if user_rating[movie] != 0 and movies_similarity[movie]>0.0:
                prediction += ( movies_similarity[movie] * ( user_rating[movie] - self.get_baseline_estimate(movie,user_id) ) )
                total_sum += movies_similarity[movie]

        if total_sum!= 0.0:
            prediction = prediction/total_sum

        # add global baseline value for the movie
        # particularly useful in the case when item-user matrix is sparse and there are few or no reviews for similar movies
        prediction_rating = self.get_baseline_estimate(movie_id,user_id) + prediction
        return prediction_rating if prediction_rating<=5.0 else 5.0

    def get_baseline_estimate(self,movie_id,user_id):
        """
        Receives a user_id and a movie_id
        Returns baseline rating value for the pair
        """
        return self.global_average + (self.global_average - self.data[user_id][0]) + (self.global_average - self.data[0][movie_id])

    def recommendation(self,user_id):
        """
        Receives a user_id
        Returns recommendation list of 10 movies for the user
        """
        user_rating = self.data[user_id,:]
        prediction = {}
        is_predicted = {}
        # get ratings for the movies user has not rated till now
        for i in range(1,len(user_rating)):
            if user_rating[i] == 0:
                precomp_user_movie_rating = self.predictions[user_id][i]
                if precomp_user_movie_rating == 0:
                    prediction[i] = self.predict(user_id,i)
                    is_predicted[i] = 1
                    self.predictions[user_id][i] = prediction[i]
                    self.write_single_rating(i, user_id, prediction[i])
                else:
                    prediction[i] = precomp_user_movie_rating;
                    is_predicted[i] = 1
                # print "rating predicted for movie " + str(i) + " for user " + str(user_id) + ":" + str( prediction[i] )
            else:
                prediction[i] = user_rating[i]
                is_predicted[i] = 0
            # print "rating for movie " + str(i) + " for user " + str(user_id) + ":" + str( prediction[i] )

            # write all the ratings for the user to file
            # print "writing reviews"
            # self.write_rating(prediction, user_id, is_predicted)

        # sort them by rating and return the indexes
        sorted_prediction = map(itemgetter(0), sorted(prediction.items(), key=itemgetter(1), reverse=True))[:300]

        final_prediction = getDiverseRecc(sorted_prediction ,self.movie_map, self.user_map, user_id)

        return final_prediction


    def write_rating(self, prediction, user_id, is_predicted):
        """
        Receives a user id, all the ratings for the user, and the information if the rating was predicted or already in the dataset
        Writes the ratings for the user to the 'ratings' file
        """
        rating_file = open('ratings', 'a')
        for movie_id in prediction.keys():
            rating_file.write( '\t'.join([str(user_id), str(movie_id), str(prediction[movie_id]), str(is_predicted[movie_id]) ]) + '\n')
        rating_file.flush()
        rating_file.close()


    def write_single_rating(self, movie_id, user_id, rating):
        """
        Write the predicted rating to the ratings file in the tab seprated format
        user_id movie_id rating 1
        1 indicates the the rating was predicted
        """
        rating_file = open('ratings', 'a')
        rating_file.write( '\t'.join([str(user_id), str(movie_id), str(rating), str(1) ]) + '\n')
        rating_file.flush()
        rating_file.close()

    def score(self, test_data):
        """
        Receives test data that is a list of user_id and movie_id tuples
        Returns the rmse value for the test data set after predicting the
        values for each and comparing it to the ground truth
        """
        predictions = []
        truth = []
        for sample in test_data:
            prediction = self.predict(sample[0],sample[1])
            print sample[0],sample[1],sample[2],prediction
            predictions += [prediction]
            truth += [sample[2]]

        rmse = sqrt(mean_squared_error(truth,predictions))
        return rmse

    def mean(values):
        """
        Returns the mean of non zero entries of a list
        """
        avg = 0.0
        total = 0.0
        count = 0.0
        for item in values:
            if item > 0:
                total += item
                count += 1
        if count <= 0:
            return avg
        else:
            avg = total/count
            return avg


    def center_value(self,value,mean):
        if value > 0:
            return value - mean
        else:
            return 0.0


    def center_rating(self,rating,mean_rating):
        """
        Method to center a users rating based on his/her other ratings
        """
        for i in range(1,len(rating)):
            rating[i] = self.center_value(rating[i],mean_rating)
        return rating


    def precompute_item_similarity(self):
        """
        Precompute item similarity matrix
        """
        l = len(self.data[0])
        # total number of items
        all_items = range(1,l)

        # print all_items
        for item_1 in all_items:
            print item_1
            movie_1 = self.data[:,item_1]
            for item_2 in all_items:
                movie_2 = self.data[:,item_2]
                if( (item_1 == item_2) or  movie_1[0] == 0.0 or  movie_2[0] == 0.0 ):
                    self.item_similarity[item_1][item_2] = 0
                elif (item_1 < item_2):
                    try:
                        similarity_value = self.similarity(movie_1,movie_2)
                        self.item_similarity[item_1][item_2] = similarity_value
                        self.item_similarity[item_2][item_1] = similarity_value
                        # break
                    except Exception as e:
                        print e
                        print item_1, item_2
        print "precomputed item similarity"
        return



    def get_similar_movies_precomp(self, movie_id):
        """
        Find similar movies given a movie id using precomputed data
        """
        item_similarity = self.item_similarity[movie_id,:]
        return np.argsort(item_similarity),item_similarity

