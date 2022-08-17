import pandas as pd
from ast import literal_eval
from datetime import datetime
from surprise import Reader, Dataset, SVD
from surprise.model_selection import KFold, cross_validate
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import combinations
from scipy.sparse import csr_matrix
# from surprise.accuracy import rmse
from collections import defaultdict
# from surprise import accuracy

class Recommendater:
    def __init__(self, user_id=0, method=''):
        self.user_id = user_id
        self.method = method

        self.links = pd.read_csv('./data/links.csv', low_memory=False)
        self.links_small = pd.read_csv('./data/links_small.csv', low_memory=False)
        self.meta_data = pd.read_csv('./data/movies_metadata.csv', low_memory=False)
        self.ratings_small = pd.read_csv('./data/ratings_small.csv', low_memory=False)
        self.meta_data['genres'] = self.meta_data['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else []).apply(lambda x: ','.join([str(i) for i in x]))
        self.movies = self.meta_data[['id', 'title', 'genres', 'vote_average', 'homepage']]

    def genres_based(self, movie_title):

        tf = TfidfVectorizer(analyzer=lambda s: (c for i in range(1,4) for c in combinations(s.split(','), r=i)))
        tfidf_matrix = tf.fit_transform(self.movies['genres'])
        cosine_sim = cosine_similarity(tfidf_matrix)
        movies = self.movies.reset_index()
        titles = movies['title']
        indices = pd.Series(movies.index, index=movies['title'])
        idx = indices[movie_title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        movie_indices = [i[0] for i in sim_scores]
        recommendations = titles.iloc[movie_indices].head(10)
        data = movies.merge(recommendations.to_frame(), left_index=True, right_index=True)
        data.rename(columns={'title_x': 'Movie Title', 'genres': 'Genres', 'vote_average': 'Vote Average', 'homepage': 'Home Page'}, inplace=True)
        data.reset_index(drop=True, inplace=True)
        return data[['Movie Title', 'Genres', 'Vote Average', 'Home Page']]

    def get_top_n(self, predictions, n=10):
        """Return the top-N recommendation for each user from a set of predictions.
        Args:
            predictions(list of Prediction objects): The list of predictions, as
                returned by the test method of an algorithm.
            n(int): The number of recommendation to output for each user. Default
                is 10.
        Returns:
        A dict where keys are user (raw) ids and values are lists of tuples:
            [(raw item id, rating estimation), ...] of size n.
        """

        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n

    def memory_based(self, user_id='1'):
        reader = Reader()
        data = Dataset.load_from_df(self.ratings_small[['userId', 'movieId', 'rating']], reader)
        svd = SVD()
        trainset = data.build_full_trainset()
        svd.fit(trainset)
        testset = trainset.build_anti_testset()
        predictions = svd.test(testset)
        top_n = self.get_top_n(predictions, 10)

        result = ""
        df_recommendation = pd.DataFrame(columns=['id'])
        if (user_id.isnumeric() and int(user_id) > 0):
            for item in top_n.get(int(user_id)):
                df_recommendation = df_recommendation.append({'id': item[0]}, ignore_index=True)

            result = df_recommendation.merge(self.movies, on='id', how='left')
            result.rename(columns={'title': 'Movie Title', 'genres': 'Genres', 'vote_average': 'Vote Average', 'homepage': 'Home Page'}, inplace=True)

        return result

    def method2(self, user_id):
        data = {
            "user id": [123, 234, 345],
            "movie title": ['Inception', 'Toy Story', 'Gone With the Wind'],
            "genres": [str(user_id) + '11', str(user_id) + '22', str(user_id) + '33']
        }
        return(pd.DataFrame(data))