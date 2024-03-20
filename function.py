from st_clickable_images import clickable_images
import streamlit as st
import pandas as pd
import requests
import joblib

from sentiment_analysis import preprocessing

svm_model = joblib.load("ml_models/svm_model.pkl")
vectorizer = joblib.load('vec_models/review_tfidf_vectorizer.pkl')

def get_movie_detail(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMGZlZTcwOGY3NGQ5NTRiYzcxOGRjNWNhYzAwOTdjZiIsInN1YiI6IjY1ZDk5M2FjMTc0OTczMDE0YWQ4NGQ2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.99DRxRjtQqy9jrWxpcvUltl2Cps3szdc854at8dHEHo"
    }

    response = requests.get(url, headers=headers)
    response = response.json()

    poster_path = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + response['poster_path']
    title = response['title']
    release_date = response['release_date']
    runtime = response['runtime']
    overview = response['overview']
    vote = response['vote_average']
    vote_count = response['vote_count']
    genre = [genre['name'] for genre in response['genres']]

    return poster_path, title, release_date, runtime, overview, vote, vote_count, genre

def click_images(id_list, text):
    file_path_list = []
    if text == 'm':
        for movie_id in id_list:
            file_path_list.append(get_movie_detail(movie_id)[0])
        
        clicked = clickable_images(
                file_path_list,
                titles=[f"Image of {get_movie_detail(movie_id)[1]}" for movie_id in id_list],
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "7px", "height": "190px"},
                )    
    elif text == 'a':
        for actor_id in id_list:
            file_path_list.append(actor_detail(actor_id)[3])

        clicked = clickable_images(
                file_path_list,
                titles=[f"Image of {actor_detail(actor_id)[0]}" for actor_id in id_list],
                div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
                img_style={"margin": "7px", "height": "190px"},
                )
    
    return clicked

def actor_detail(actor_id):

    url = f"https://api.themoviedb.org/3/person/{actor_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMGZlZTcwOGY3NGQ5NTRiYzcxOGRjNWNhYzAwOTdjZiIsInN1YiI6IjY1ZDk5M2FjMTc0OTczMDE0YWQ4NGQ2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.99DRxRjtQqy9jrWxpcvUltl2Cps3szdc854at8dHEHo"
    }

    response = requests.get(url, headers=headers)
    response = response.json()

    name = response['name']
    birthday = response['birthday']
    biography = response['biography']
    profile = "https://media.themoviedb.org/t/p/w300_and_h450_bestv2" + str(response['profile_path'])

    return name, birthday, biography, profile

def get_actor(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMGZlZTcwOGY3NGQ5NTRiYzcxOGRjNWNhYzAwOTdjZiIsInN1YiI6IjY1ZDk5M2FjMTc0OTczMDE0YWQ4NGQ2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.99DRxRjtQqy9jrWxpcvUltl2Cps3szdc854at8dHEHo"
    }

    response = requests.get(url, headers=headers)
    response = response.json()

    actor_id_list = []
    for actor in response['cast']:
        actor_id_list.append(actor['id'])

    if len(actor_id_list) > 5:
        actor_id_list = actor_id_list[0:5]
    else:
        actor_id_list
        
    return actor_id_list

def get_review(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMGZlZTcwOGY3NGQ5NTRiYzcxOGRjNWNhYzAwOTdjZiIsInN1YiI6IjY1ZDk5M2FjMTc0OTczMDE0YWQ4NGQ2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.99DRxRjtQqy9jrWxpcvUltl2Cps3szdc854at8dHEHo"
    }

    response = requests.get(url, headers=headers)
    response = response.json()

    reviews = []
    for review in response['results']:
        content = ''.join(s for s in review['content'] if ord(s)>31 and ord(s)<126)
        sentiment = get_sentiment(content)
        reviews.append([review['author'], content, eval(str(review['author_details']['rating'])), sentiment])

    reviews = pd.DataFrame(data = reviews, columns=['Author', 'Review', 'Rating', 'Sentiment'])

    return reviews

def get_sentiment(text):
    vector = vectorizer.transform([text]).toarray()
    result = svm_model.predict(vector)
    return result[0]