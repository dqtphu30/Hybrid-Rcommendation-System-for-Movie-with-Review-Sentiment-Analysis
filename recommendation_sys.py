import pandas as pd
import numpy as np
import joblib


svd = joblib.load("recommender_dict/svd_recommender.pkl")
cosine_sim = joblib.load("recommender_dict/similarity.pkl")
smd = joblib.load("recommender_dict/movie_dict.pkl")

titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])

def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

links = pd.read_csv('./Data/links_small.csv')
links = links.drop(columns=['imdbId'])
links = links.dropna(ignore_index=True)
links.columns = ['Movie_Index', 'id']
id_map = links.astype('int')
id_map = id_map.merge(smd[['title', 'id']], on='id').set_index('title')

indices_map = id_map.set_index('id')

def hybrid(userId, title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    movies = smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'id']]
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map.loc[x]["Movie_Index"]).est)
    movies = movies.sort_values('est', ascending=False)
    return movies.head(5)