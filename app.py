import pickle
import streamlit as st
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout, HTTPError, RequestException

def fetch_poster(movie_id):
    api_key = "025cad5038a227c8054c596e53ffc12d"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()
        print(data)
        poster_path = data.get('poster_path',None)
        
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/original/{poster_path}"
            return full_path
        else:
            return None
    except ReadTimeout:
        st.error("The server did not send any data in the allotted amount of time. Please try again later.")
        return None
    except ConnectTimeout:
        # st.error("Connection to the API timed out. Please try again later.")
        return None
    except HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        return None
    except RequestException as err:
        st.error(f"Error occurred: {err}")
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        # print(poster_url)
        if poster_url:
            recommended_movie_posters.append(poster_url)
        else:
            recommended_movie_posters.append("https://via.placeholder.com/500")  # Placeholder image
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names

st.header('Movie Recommender System Using Machine Learning')
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            # st.image(recommended_movie_posters[idx])
