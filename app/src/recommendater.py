import pandas as pd
from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
# from surprise import Reader, Dataset, SVD
# from surprise.model_selection import KFold, cross_validate
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import combinations
# from surprise.accuracy import rmse
# from collections import defaultdict
# from surprise import accuracy

class Recommendater:
    def __init__(self, user_id, method=''):
        self.user_id = user_id
        self.method = method

        self.links = pd.read_csv('./data/links.csv', low_memory=False)
        self.links_small = pd.read_csv('./data/links_small.csv', low_memory=False)
        self.meta_data = pd.read_csv('./data/movies_metadata.csv', low_memory=False)
        self.ratings_small = pd.read_csv('./data/ratings_small.csv', low_memory=False)


    def genres_base(self, movie_title):
        self.meta_data['genres'] = self.meta_data['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else []).apply(lambda x: ','.join([str(i) for i in x]))
        movies = self.meta_data[['id', 'title', 'genres']]
        # Find the sets of combinations of genre
        tf = TfidfVectorizer(analyzer=lambda s: (c for i in range(1,4) for c in combinations(s.split(','), r=i)))
        tfidf_matrix = tf.fit_transform(movies['genres'])
        cosine_sim = cosine_similarity(tfidf_matrix)
        movies = movies.reset_index()
        titles = movies['title']
        indices = pd.Series(movies.index, index=movies['title'])
        idx = indices[movie_title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        movie_indices = [i[0] for i in sim_scores]
        recommendations = titles.iloc[movie_indices].head(10)
        return movies.merge(recommendations.to_frame(), left_index=True, right_index=True)[['title_x', 'genres']]


    def method1(self, user_id):
        data = {
            "user id": [420, 380, 390],
            "movie title": ['The godfather', 'Forrest Gump', 'The Dark Knight'],
            "genres": [str(user_id) + '11', str(user_id) + '22', str(user_id) + '33']
        }
        return(pd.DataFrame(data))

    def method2(self, user_id):
        data = {
            "user id": [123, 234, 345],
            "movie title": ['Inception', 'Toy Story', 'Gone With the Wind'],
            "genres": [str(user_id) + '11', str(user_id) + '22', str(user_id) + '33']
        }
        return(pd.DataFrame(data))