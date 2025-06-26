import pandas as pd
import os
import json

# Path to TMDB movie data
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/tmdb_5000_movies.csv")

# Load dataset
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = pd.DataFrame()

# Parse 'genres' column to extract genre names
def parse_genres(genre_str):
    try:
        genres = json.loads(genre_str.replace("'", '"'))
        return [g["name"] for g in genres]
    except:
        return []

df["genre_names"] = df["genres"].apply(parse_genres)

# Construct poster URL (using TMDb image base if poster_path available)
def get_poster_url(title):
    # TMDB 5000 dataset doesn’t have poster_path by default
    # You can manually add a column or use placeholder logic
    placeholder_url = "https://via.placeholder.com/100x150?text=" + title.replace(" ", "+")
    return placeholder_url

df["poster_url"] = df["title"].apply(get_poster_url)

# Mood to genre mapping
mood_genre_map = {
    "Happy": ["Comedy", "Adventure", "Family"],
    "Emotional": ["Drama", "Romance"],
    "Curious": ["Mystery", "Sci-Fi", "Thriller"],
    "Casual": ["Animation", "Family", "Fantasy"]
}

# Suggest the best movie from the given list based on mood
def suggest_from_choices(movie_list, mood):
    mood_genres = mood_genre_map.get(mood, [])
    matches = []

    for title in movie_list:
        movie = df[df["title"].str.lower() == title.lower()]
        if not movie.empty:
            row = movie.iloc[0]
            genres = row["genre_names"]
            overlap = set(genres).intersection(set(mood_genres))
            score = len(overlap)
            matches.append({
                "title": row["title"],
                "poster_url": row["poster_url"],
                "description": row["overview"] if isinstance(row["overview"], str) else "No description available.",
                "score": score,
                "reason": f"Matches your mood ({mood}) with genre(s): {', '.join(overlap) if overlap else 'None'}"
            })

    if not matches:
        return {
            "title": "No Match Found",
            "poster_url": "",
            "description": "We couldn't find these movies in our database.",
            "reason": "Try using exact movie titles from TMDB 5000 dataset."
        }

    # Sort by score (matching mood genres), then by popularity (if needed)
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[0]
