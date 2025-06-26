import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recommender.content_based import get_content_recommendations
from recommender.decision_maker import suggest_from_choices

# 🎨 Custom CSS for Dark Mode
st.markdown("""
    <style>
    body {
        background-color: #181818;
        color: white;
    }
    .reportview-container {
        background: #181818;
    }
    .sidebar .sidebar-content {
        background: #202020;
    }
    .stButton>button {
        background-color: #cc0000;
        color: white;
    }
    .movie-card {
        background-color: #282828;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        display: flex;
        gap: 1rem;
    }
    .movie-title {
        font-size: 1.3rem;
            color: #f0f0f0;
        font-weight: bold;
    }
    .reason-text {
        font-size: 1rem;
        color: #aaa;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Cinevark")
st.markdown("_Explore. Decide. Watch. — Powered by ASRAccelet_")
st.markdown("_____Developed with ❤️ by shankar-irla_____")

# Sidebar
st.sidebar.title("🧭 Navigation")
mode = st.sidebar.radio("Choose Mode", ["🎯 Recommend Me", "🤔 Help Me Choose"])

# Mode 1: Recommend based on genre + mood
if mode == "🎯 Recommend Me":
    genre = st.sidebar.selectbox("Choose Genre", ["Action", "Romance", "Comedy", "Thriller", "Family"])
    mood = st.sidebar.selectbox("Your Mood Now", ["Happy", "Sad", "Excited", "Relaxed", "Emotional", "Curious", "Light-hearted"])

    if st.sidebar.button("Recommend Now"):
        results = get_content_recommendations(genre, mood)

        st.subheader("🎥 Top Picks For You")
        for movie in results:
            poster = movie.get("homepage") or "https://via.placeholder.com/100x150" 
            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}" width="100">
                <div>
                    <div class="movie-title">{movie['title']}</div>
                    <div class="reason-text">{movie['description']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Mode 2: Decision-maker (unique feature)
elif mode == "🤔 Help Me Choose":
    input_movies = st.text_input("Enter 2–5 Movie Names (comma separated)")
    mood = st.selectbox("Your Mood", ["Happy", "Emotional", "Curious", "Casual"])

    if st.button("Choose Best for Me"):
        movie_list = [m.strip() for m in input_movies.split(",") if m.strip()]
        if len(movie_list) < 2:
            st.warning("Please enter at least 2 movies.")
        else:
            pick = suggest_from_choices(movie_list, mood)
            poster = pick.get("poster_url") or "https://via.placeholder.com/110x160"
            st.success(f"Best Pick: 🎯 {pick['title']}")
            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}" width="110">
                <div>
                    <div class="movie-title">{pick['title']}</div>
                    <div class="reason-text">{pick['reason']}</div>
                    <div class="reason-text">{pick['description']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
