import streamlit as st
import requests
from urllib.parse import quote
from recommender import recommend, movies_list
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get TMDB API key from .env file
API_KEY = os.getenv("TMDB_API_KEY")

# Streamlit page settings
st.set_page_config(page_title="Movie Recommender", layout="wide")

# App title
st.title("🎬 AI Movie Recommendation System")


# Clean movie title (remove year)
def clean_title(title):
    if "(" in title:
        title = title.split("(")[0]
    return title.strip()


#Fetch movie details from TMDB
def fetch_movie_details(movie_name):

    try:
        query = quote(clean_title(movie_name))

        url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={API_KEY}&query={query}"
        )

        res = requests.get(url, timeout=5)
        data = res.json()

        if data.get("results"):

            movie = None

            #Find best matching movie
            for result in data["results"]:

                if clean_title(movie_name).lower() in result["title"].lower():
                    movie = result
                    break

            # If no exact match found
            if movie is None:
                movie = data["results"][0]

            poster_path = movie.get("poster_path")
            rating = movie.get("vote_average", "N/A")
            release_date = movie.get("release_date", "N/A")
            overview = movie.get(
                "overview",
                "No description available."
            )

            poster_url = (
                "https://image.tmdb.org/t/p/w500" + poster_path
                if poster_path
                else "https://via.placeholder.com/300x450?text=No+Poster"
            )

            return poster_url, rating, release_date, overview

        return (
            "https://via.placeholder.com/300x450?text=No+Poster",
            "N/A",
            "N/A",
            "No description available."
        )

    except Exception:

        return (
            "https://via.placeholder.com/300x450?text=Error",
            "N/A",
            "N/A",
            "Error fetching details."
        )
#Select movie
selected_movie = st.selectbox(
    "Select a movie",
    movies_list
)

#Recommend button
if st.button("Recommend"):

    with st.spinner("Finding recommendations..."):

        recommendations = recommend(selected_movie)

        if recommendations:

            st.subheader("🎯 Recommended Movies")

            cols = st.columns(5)

            for i, movie in enumerate(recommendations[:5]):

                poster, rating, release, overview = fetch_movie_details(movie)

                with cols[i]:

                    st.markdown(f"### {movie}")

                    st.image(poster, width=200)

                    st.caption(f"⭐ Rating: {rating}")

                    st.caption(f"📅 Release: {release}")

        else:
            st.warning("Movie not found!")


# 💬 Mood-based suggestions
st.subheader("💬 Ask for Suggestions")

user_input = st.text_input(
    "Type mood (e.g., action, comedy, romantic)"
)

if user_input:

    filtered_movies = [
        movie for movie in movies_list
        if user_input.lower() in movie.lower()
    ]

    if filtered_movies:

        st.subheader("🎥 Movies You May Like")

        cols = st.columns(5)

        for i, movie in enumerate(filtered_movies[:5]):

            poster, rating, release, overview = fetch_movie_details(movie)

            with cols[i]:

                st.markdown(f"### {movie}")

                st.image(poster, width=200)

                st.caption(f"⭐ Rating: {rating}")

                st.caption(f"📅 Release: {release}")

    else:
        st.write("No movies found for this mood.")