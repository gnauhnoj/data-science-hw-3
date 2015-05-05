# Data-Science-hw-3

## Adding the dataset:

- Download the 100k reviews data file from [here](http://files.grouplens.org/datasets/movielens/ml-100k.ziphttp://files.grouplens.org/datasets/movielens/ml-100k.zip)
- Unzip the downloaded file inside of a subdirectory of root "data/".


## Recommendation System:

Running the recommedation takes a long time so we precomputed the missing (predicted) ratings in the dataset using the collaborative filtering method discussed in our writeup and stored the results in a 'ratings' file.

Follow these steps to get recommendations given a set of users:
- Download the 'ratings' file from [here](https://github.com/gnauhnoj/data-science-hw-3/blob/master/ratings) and put it inside the folder with rest of the files.
- Open the file ml_recommender.py.
- You can specify the users for which you want recommendations by adding them to the 'users_to_recommend' list on line 42
- Uncomment the line in main that calls get_recommendations function on line 44
The result is the 10 (or less depending on the number of reviews the user has already made) recommendations for each user which are printed in the console.

**Sample Output**:
![alt tag](https://github.com/gnauhnoj/data-science-hw-3/blob/master/ouput.png)

**NOTE**: The solution works regardless of the presence of the ratings file, but the presence of the file enables the system to give results instantaneously.

## Train and test

Follow these steps to do a training and testing on the dataset:
- Open the file ml_recommender.py.
- Uncomment the line in main that calls train_and_test function. It takes a while to run and in the end prints the RMSE value for the test datset on line 43.