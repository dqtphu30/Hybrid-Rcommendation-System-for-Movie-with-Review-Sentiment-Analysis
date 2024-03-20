from streamlit_modal import Modal
import streamlit as st
import joblib

from function import *
from recommendation_sys import *

user_id = st.number_input("Insert a user id number", min_value = 1, value= None , placeholder="Type a number...")

movie_list = joblib.load("C:/Users/thien/Downloads/MovieReview/recommender_dict/movie_title_dict.pkl")
smd = joblib.load("C:/Users/thien/Downloads/MovieReview/recommender_dict/movie_dict.pkl")

print("Hello 1!")

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

print("Hello 2!")

if st.session_state.clicks == True:
    print("Hello 3!")

    movie_id_find = smd[smd['title']==selected_movie_name]["id"].iloc[0]

    st.title(get_movie_detail(movie_id_find)[1].upper())

    col1, col2 = st.columns((1,2))
    with col1:
        st.image(get_movie_detail(movie_id_find)[0])
    with col2:
        st.markdown(f"**Title:** {get_movie_detail(movie_id_find)[1]}")
        st.markdown(f"**Release day:** {get_movie_detail(movie_id_find)[2]}")
        st.markdown(f"**Popularity:** {get_movie_detail(movie_id_find)[3]}")
        st.markdown(f"**Overview:** {get_movie_detail(movie_id_find)[4]}")
        st.markdown(f"**Score:** {get_movie_detail(movie_id_find)[5]}/10⭐ ({get_movie_detail(movie_id_find)[6]} ratings)")
        st.markdown(f"**Genre:** {get_movie_detail(movie_id_find)[7]}")


    st.header(f"**Top 5 Cast**")
    actor_list = get_actor(movie_id_find)
    clicked_1 = click_images(actor_list, 'a')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        #st.image(actor_detail(actor_list[0])[3])
        st.markdown(actor_detail(actor_list[0])[0])
    with col2:
        #st.image(actor_detail(actor_list[1])[3])
        st.markdown(actor_detail(actor_list[1])[0])
    with col3:
        #st.image(actor_detail(actor_list[2])[3])
        st.markdown(actor_detail(actor_list[2])[0])
    with col4:
        #st.image(actor_detail(actor_list[3])[3])
        st.markdown(actor_detail(actor_list[3])[0])
    with col5:
        #st.image(actor_detail(actor_list[4])[3])
        st.markdown(actor_detail(actor_list[4])[0])

    st.header(f"**Review**")
    st.table(get_review(movie_id_find))


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

    movie_id_clicked = movie_id_recommender[clicked_2]
    movie_id_find = movie_id_clicked

    if clicked_2 > -1:
        print("Hello 4!")
        st.session_state['selection'] = smd.index[smd['id']==movie_id_clicked].tolist()[0]
        st.markdown(clicked_2)

else:
    st.header(f"**Welcome")
