import streamlit as st
import pickle
import bz2
import requests

movies_lists = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(bz2.BZ2File("similarity.pkl", "rb"))
movies_list = movies_lists["title"].values


def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]


def recommend(movie):
    # print(movies_list)
    movie_index = movies_lists[movies_lists["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_listed = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_listed:
        movie_id = movies_lists.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies_lists.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters


st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Which movie would you like to watch ?", movies_list)
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
