import numpy as np
from scipy.stats.stats import pearsonr
from operator import itemgetter

class collaborative_filtering:
    def __init__(self, data):
        """
        initialize the matrix for filtering
        TODO: get test and train data separately
        """
        self.data = data
        items = len(data[0])
        self.item_similarity = np.zeros((items, items), dtype=float)

    def precompute_item_similarity(self):
        """
        Precompute item similarity matrix
        """
        # total number of items
        all_items = range(1,int(l*0.2))
        
        # print all_items
        for item_1 in all_items:
            movie_1 = self.data[:,item_1]
            for item_2 in all_items:
                movie_2 = self.data[:,item_2]
                if( (item_1 == item_2) or  movie_1[0] == 0.0 or  movie_2[0] == 0.0 ):
                    self.item_similarity[item_1][item_2] = 0
                elif (item_1 < item_2):
                    try:
                        self.item_similarity[item_1][item_2] = self.similarity(self.data[:,item_1],self.data[:,item_2])
                        self.item_similarity[item_2][item_1] = self.similarity(self.data[:,item_1],self.data[:,item_2])
                    except Exception as e:
                        print item_1, item_2
                        print self.data[:,item_1]
                        print self.data[:,item_2]
        print "precomputed item similarity"
        return

    def similarity(self, item_1, item_2):
        """
        Method to compute similarity between 2 items
        Assuming pearson for now
        """
        similarity_value = pearsonr(item_1,item_2)[0]
        return similarity_value

    def get_similar_movies(self, movie_id):
        """
        Find similar movies given a movie id
        """
        item_similarity = self.item_similarity[movie_id,:]
        return np.argsort(item_similarity),item_similarity
    
    def predict(self,user_id,movie_id):
        """
        given a user_id and a movie_id
        predict the rating for the user
        Assuming item-item 
        """
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

    def score(self, test):
        return