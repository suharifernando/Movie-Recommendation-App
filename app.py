from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__, static_folder='static')

# --- STEP 1: LOAD DATA ---
data = df = pd.read_csv('C:/Projects/Movie Recomendor/movies.csv')

df = pd.DataFrame(data)

# Pre-process genres for the recommendation engine
df['genres_processed'] = df['genres'].str.replace('|', ' ', regex=False)

# Build the Similarity Engine
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['genres_processed'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# --- STEP 2: SMART SEARCH LOGIC ---

def find_best_movie_match(user_input):
    user_input = user_input.lower().strip()
    all_titles = df['title'].str.lower().tolist()
    original_titles = df['title'].tolist()

    if user_input in all_titles:
        idx = all_titles.index(user_input)
        return original_titles[idx]

    partial_matches = [t for t in original_titles if user_input in t.lower()]
    if partial_matches:
        return partial_matches[0]

    fuzzy_matches = difflib.get_close_matches(user_input, original_titles, n=1, cutoff=0.3)
    if fuzzy_matches:
        return fuzzy_matches[0]

    return None

def get_recommendations(target_title):
    # Find the index of the movie
    idx = df[df['title'].str.lower() == target_title.lower()].index[0]

    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 5 (excluding itself)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    
    # FIX: Extract both Title and Genre
    recommended_df = df.iloc[movie_indices][['title', 'genres']]
    
    # Convert to list of dictionaries and replace '|' with comma for better reading
    results = []
    for _, row in recommended_df.iterrows():
        results.append({
            "title": row['title'],
            "genres": row['genres'].replace('|', ', ')
        })
    
    return results

# --- STEP 3: ROUTES ---

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/recommend', methods=['GET'])
def recommend():
    query = request.args.get('movie')
    if not query:
        return jsonify({"error": "No input provided"}), 400

    matched_title = find_best_movie_match(query)

    if not matched_title:
        return jsonify({"error": f"Could not find '{query}'. Try typing a part of the name."}), 404

    recommendations = get_recommendations(matched_title)
    return jsonify({
        "matched_with": matched_title,
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)