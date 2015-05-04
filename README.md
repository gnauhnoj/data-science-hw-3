# data-science-hw-3

Adding the dataset:

- Download the 100k reviews data set from [here](http://files.grouplens.org/datasets/movielens/ml-100k.ziphttp://files.grouplens.org/datasets/movielens/ml-100k.zip)
- Unzip the downoladed folder inside it.


Recommendation System:

Running the recommedation takes time so we precomputed the missing ratings in the dataset using collaborative filtering method and stored the results in a 'ratings' file.

Follow the steps to get recommendations for a set of users
- Download the file from here: and put it inside the folder.
- Open the file ml_recommender.py.
- You can specify the users for which you want recommendations by adding them to the 'users_to_recommend' list.
- Uncomment the line in main that calls get_recommendations function. 
The result is the recommendation for each user.

NOTE: The solution works regardless of the presence of the ratings file, but the presence of the file enables the system to give results instantaneously.

Follow the steps to do a training and testing on the dataset
1. Open the file ml_recommender.py.
2. Uncomment the line in main that calls train_and_test function. It takes a while to run and in the end prints the RMSE value for the test datset.