# 🎬 Movie Recommendation App

A simple web application that suggests movies based on genre similarity using **Content-Based Filtering**. The app features a "smart search" that handles typos and partial movie titles.

## 🚀 Features
- **Smart Search:** Finds movies even if you make typos or don't type the full year.
- **Genre Matching:** Uses TF-IDF and Cosine Similarity to recommend movies with similar themes.
- **Modern UI:** A clean, Netflix-inspired dark mode interface.
- **Detailed Results:** Shows movie titles along with their genre tags.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Pandas, Scikit-learn
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

## 📋 Installation & Setup

1. **Install Dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install flask pandas scikit-learn
   ```

2. **Project Structure:**
   Ensure your files are organized like this:
   ```text
   movie-app/
   ├── app.py          
   ├── index.html      
   └── movies.csv 
   ```

3. **Run the App:**
   ```bash
   python app.py
   ```

4. **Access the App:**
   Open your browser and go to: `http://127.0.0.1:5000`

## 📊 Dataset
The app currently uses a sample dataset from `https://grouplens.org/datasets/movielens/`
To use your own data, ensure your `movies.csv` has the following columns:
- `title`: The name of the movie (e.g., "Toy Story (1995)")
- `genres`: Genres separated by pipes (e.g., "Animation|Comedy|Children")

## 💡 How it Works
1. **Vectorization:** The system converts text genres into numerical vectors using `TfidfVectorizer`.
2. **Similarity:** It calculates the "distance" between these vectors using `linear_kernel`.
3. **Fuzzy Matching:** Using Python's `difflib`, the app guesses what you meant if you misspell a movie name.
