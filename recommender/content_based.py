import pandas as pd
import os
import ast

# Path to TMDb 5000 dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/tmdb_5000_movies.csv")

# Load movie data
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = pd.DataFrame()

# Extract genre names from JSON string
def extract_genre_names(genre_str):
    try:
        genres = ast.literal_eval(genre_str)
        return [g["name"] for g in genres]
    except:
        return []

# Add genre_names and poster_url columns
df["genre_names"] = df["genres"].apply(extract_genre_names)
df["poster_url"] = "https://via.placeholder.com/300x450?text=" + df["title"].str.replace(" ", "+")

# Define moods and related genres
mood_genre_map = {
    "Happy": ["Comedy", "Adventure", "Family"],
    "Sad": ["Drama", "Romance"],
    "Excited": ["Action", "Thriller", "Sci-Fi"],
    "Relaxed": ["Animation", "Fantasy", "Documentary"],
    "Emotional": ["Romance", "Drama"],
    "Curious": ["Mystery", "Sci-Fi", "Thriller"],
    "Light-hearted": ["Comedy", "Family", "Animation"]
}

def get_content_recommendations(genre, mood, top_n=5):
    genre = genre.lower()
    mood_genres = mood_genre_map.get(mood, [])

    # Filter rows where genre matches and at least one mood genre is present
    filtered = df[
        df["genre_names"].apply(lambda x: genre in [g.lower() for g in x]) &
        df["genre_names"].apply(lambda x: any(mg in x for mg in mood_genre_map.get(mood, [])))
    ]

    if filtered.empty:
        return [{
            "title": "No matching movies",
            "poster_url": "",
            "description": "Try changing your genre or mood selection."
        }]

    # Sort and get top results
    sorted_df = filtered.sort_values(by="popularity", ascending=False).head(top_n)

    results = []
    for _, row in sorted_df.iterrows():
        results.append({
            "title": row["title"],
            "poster_url": row["poster_url"],
            "description": (row["overview"][:200] + "...") if isinstance(row["overview"], str) else "No description available."
        })

    return results
