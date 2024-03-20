from streamlit_modal import Modal
import streamlit as st
import joblib

from function import *
from recommendation_sys import *

user_id = st.number_input("Insert a user id number", min_value = 1, value= None , placeholder="Type a number...")

movie_list = joblib.load("C:/Users/thien/Downloads/MovieReview/recommender/movie_title_dict.pkl")
smd = joblib.load("C:/Users/thien/Downloads/MovieReview/recommender/movie_dict.pkl")

# Initialize the session state
if 'selection' not in st.session_state:
    st.session_state['selection'] = None

selected_movie_name = st.selectbox('Phim cần tìm:',
                                   movie_list,
                                   index = st.session_state['selection'],
                                   placeholder= "Nhập và chọn tên phim")

if 'clicks' not in st.session_state:
    st.session_state.clicks = False

def click():
    st.session_state.clicks = True

def unclick():
    st.session_state.clicks = False

left, right = st.columns(2)
left.button(f'Find', on_click=click)
right.button(f'Reset', on_click=unclick)

if st.session_state.clicks == True:
    st.header(f"**Recommendation**")
    movie_id_recommender = hybrid(user_id, selected_movie_name)['id'].tolist()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(get_movie_detail(movie_id_recommender[0])[1])
    with col2:
        st.markdown(get_movie_detail(movie_id_recommender[1])[1])
    with col3:
        st.markdown(get_movie_detail(movie_id_recommender[2])[1])
    with col4:
        st.markdown(get_movie_detail(movie_id_recommender[3])[1])
    with col5:
        st.markdown(get_movie_detail(movie_id_recommender[4])[1])

    clicked_2 = click_images(movie_id_recommender, 'm')
    st.markdown(clicked_2)
    movie_id_clicked = movie_id_recommender[1+clicked_2]
    st.markdown(movie_id_clicked)

    if clicked_2 >= -1:
        st.session_state['selection'] = smd.index[smd['id']==movie_id_clicked].tolist()[0]

else:
    st.header(f"**Welcome")
