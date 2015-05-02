import numpy as np
from scipy.stats.stats import pearsonr
from operator import itemgetter
from sklearn.metrics import mean_squared_error
from math import sqrt


class collaborative_filtering:
    def __init__(self, data):
        """
        initialize the matrix for filtering
        TODO: get test and train data separately
        """
        self.put_data(data)

    def get_data(self):
        return self.data


    def put_data(self,data):
        self.data = data
        self.n_movies = len(data[0])
        self.item_similarity = np.zeros((self.n_movies, self.n_movies), dtype=float)
        return


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
                        # print self.data[:,item_1]
                        # print self.data[:,item_2]
                        # break
            # break
        print "precomputed item similarity"
        return


    def similarity(self, item_1, item_2):
        """
        Method to compute similarity between 2 items
        Assuming pearson for now
        """
        # print "get pearson"
        new_1 = []
        new_2 = []
        for i in range(1,len(item_1)):
            if (item_1[i] != 0) or (item_2[i] != 0):
                new_1.append(item_1[i])
                new_2.append(item_2[i])
        # zero_indices_1 = np.where(item_1 == 0.0)[0]
        # zero_indices_2 = np.where(item_2 == 0.0)[0]
        # all_zero_indices = np.concatenate([zero_indices_1,zero_indices_1])
        # if len(all_zero_indices) == len(item_1):
        #     return 0.0
        # remove_indices = np.unique(all_zero_indices)
        # new_1 = np.delete(item_1,remove_indices)
        # new_2 = np.delete(item_2,remove_indices)
        if (len(new_1) == 0) or (len(new_2) == 0) or (sum(new_1) == 0.0) or (sum(new_2) == 0.0):
            return 0.0
        similarity_value = pearsonr(new_1,new_2)[0]
        return similarity_value


    def get_similar_movies_precomp(self, movie_id):
        """
        Find similar movies given a movie id using precomputed data
        """
        item_similarity = self.item_similarity[movie_id,:]
        return np.argsort(item_similarity),item_similarity
    
    def get_similar_movies(self, item_1):
        """
        Find similar movies given a movie id
        """
        all_items = range(1,self.n_movies)
        movie_1 = self.data[:,item_1]
        # print movie_1
        similarities = np.zeros(self.n_movies, dtype=float)
        for item_2 in all_items:
            movie_2 = self.data[:,item_2]
            if( (item_1 == item_2) or  movie_1[0] == 0.0 or  movie_2[0] == 0.0 ):
                similarities[item_2] = 0
            else:
                try:
                    similarities[item_2] = self.similarity(movie_1,movie_2)
                    # print similarities[item_2]
                    # break
                except Exception as e:
                    print e
                    print item_1, item_2
        # print similarities
        return np.argsort(similarities),similarities


    def predict(self,user_id,movie_id):
        """
        given a user_id and a movie_id
        predict the rating for the user
        Assuming item-item 
        """
        # print "predict"
        # get similarity value of all other movies(items) for the given movie
        # TODO: change it to top k if needed
        similar_movies, movies_similarity = self.get_similar_movies(movie_id)

        # get all the ratings posted by the user
        user_rating = self.data[user_id,:]

        prediction = 0.0
        total_sum = 0.0
        # for s in movies_similarity:
        #     if s>0:
        #         total_sum += s 

        # do a weighted sum of users existing reviews
        # weights are based on the similarity values
        # if (total_sum != 0.0):
        for movie in similar_movies:
            # print prediction.keys()
            if user_rating[movie] != 0 and movies_similarity[movie]>0.0:
                prediction += (movies_similarity[movie]*user_rating[movie])
                print prediction
                total_sum += movies_similarity[movie]
        
        if total_sum!= 0.0:
            prediction = prediction/total_sum

        return prediction


    def recommendation(self,user_id):
        # get similarity value of all other movies(items) for the given movie
        # TODO: change it to top k if needed
        similar_movies, movies_similarity = self.get_similar_movies(movie_id)

        # get all the ratings posted by the user
        user_rating = self.data[user_id,:]

        prediction = {}
        total_sum = sum(movies_similarity) 
        # do a weighted sum of users existing reviews
        # weights are based on the similarity values
        for movie in similar_movies:
            # print prediction.keys()
            if user_rating[movie] != 0:
                if movie in prediction.keys():
                    prediction[movie] += (movies_similarity[movie]*user_rating[movie])/total_sum
                else:
                    prediction[movie] = (movies_similarity[movie]*user_rating[movie])/total_sum 

        # sort prediction by rating value
        # sorted_prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        sorted_prediction = map(itemgetter(0), sorted(prediction.items(), key=itemgetter(1), reverse=True))[:5]
        #return top 5
        return sorted_prediction


    def score(self, test_data):
        """
        Returns the rmse value for the test data
        """
        predictions = []
        truth = []
        for sample in test_data:
            prediction = self.predict(sample[0],sample[1])
            print sample[0],sample[1],sample[2],prediction
            predictions += [prediction]
            truth += [sample[2]]

        rms = sqrt(mean_squared_error(truth,predictions))
        return rms