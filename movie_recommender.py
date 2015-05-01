import numpy as np

class collaborative_filtering:
    def __init__(self, data):
        """
        initialize the matrix for filtering
        TODO: get test and train data separately
        """
        self.data = data
        items = len(data[0])
        self.item_similarity = np.zeros((items + 1, items +1), dtype=float)

    def precompute_item_similarity(self):
    	"""
    	Precompute item similarity matrix
    	"""
    	# total number of items
    	all_items = range(len(self.data[0]))
    	for item_1 in all_items:
    		for item_2 in items:
    			if(item_1 == item_2):
    				self.item_similarity[item_1][item_2] = 0
    			else:
    				self.item_similarity[item_1][item_2] = similarity(item_1,item_2)
    	return

    def similarity(self, item_1, item_2):
    	"""
    	Method to compute similarity between 2 items
    	"""
    	return similarity_value

    def predict(user_id,movie_id):
    	"""
    	given a user_id and a movie_id
    	predict the rating for the user
    	Assuming item-item 
    	"""
    	# get similarity value of all other movies(items) for the given movie
    	# TODO: change it to top k if needed

    	# get all the ratings for the user
    	# do a weighted sum of users existing reviews
    	# weights are based on the similarity values

    	return