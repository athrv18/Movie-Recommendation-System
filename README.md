# 🎬 Movie Recommendation System

A full-stack movie recommendation application that combines a **Streamlit interface**, **FastAPI backend**, **TF-IDF-based movie similarity**, and **TMDB movie data** to help users search for movies, explore movie information, and discover similar titles.

The application uses precomputed TF-IDF resources for local content-based recommendations while TMDB is used for movie search, posters, details, categories, and genre-based recommendations. ([GitHub][1])

---

## ✨ Features

* 🔎 Search movies by title
* 🎬 View movie posters and release information
* 📖 View movie details and overview
* 🤖 Get similar movie recommendations using TF-IDF
* 🎭 Get genre-based movie recommendations
* 🔥 Browse trending movies
* ⭐ Browse popular and top-rated movies
* 🎞️ Browse currently playing and upcoming movies
* 🖼️ Display TMDB movie posters and backdrops
* 📱 Responsive Streamlit movie interface
* ⚡ FastAPI backend with dedicated API endpoints
* ❤️ Interactive movie discovery experience

The Streamlit application provides movie search, category selection, movie cards, and navigation to movie details, while the FastAPI service exposes TMDB, genre, and TF-IDF recommendation functionality. ([GitHub][1])

---

## 🛠️ Tech Stack

| Category          | Technologies                            |
| ----------------- | --------------------------------------- |
| Frontend          | Streamlit                               |
| Backend           | FastAPI, Uvicorn                        |
| Machine Learning  | Scikit-learn, TF-IDF, Cosine Similarity |
| Data Processing   | Pandas, NumPy, SciPy                    |
| External API      | TMDB API                                |
| HTTP/API Requests | Requests, HTTPX                         |
| Configuration     | Python Dotenv                           |
| Deployment        | Render                                  |

The dependency versions are defined in `requirements.txt`, including FastAPI, Uvicorn, Streamlit, Pandas, NumPy, SciPy, Scikit-learn, python-dotenv, and Requests. ([GitHub][2])

---

## 🧠 How It Works

### 1. User Searches for a Movie

The user enters a movie title in the Streamlit interface.

The application sends the search request to the FastAPI backend, which communicates with TMDB to find matching movies. ([GitHub][1])

### 2. Movie Information is Retrieved

TMDB provides information such as:

* Movie title
* Poster
* Release date
* Rating
* Overview
* Genres
* Backdrop

The backend converts this information into structured movie objects for the Streamlit interface. ([GitHub][3])

### 3. TF-IDF Recommendation

The project contains precomputed:

* TF-IDF vectorizer
* TF-IDF matrix
* Movie index mapping
* Movie dataframe

When a movie is selected, its TF-IDF vector is compared with the vectors of other movies. ([GitHub][3])

### 4. Cosine Similarity

The system calculates similarity scores between the selected movie and other movies using the TF-IDF matrix.

Movies with higher similarity scores are returned as recommendations. ([GitHub][3])

### 5. Recommendations are Displayed

The recommended movies are presented through the Streamlit interface with movie information and posters.

---

## 🤖 Recommendation Method

The project uses **TF-IDF (Term Frequency–Inverse Document Frequency)** with similarity calculations for content-based movie recommendations.

The FastAPI backend loads the precomputed TF-IDF resources from:

```text
df.pkl
indices.pkl
tfidf.pkl
tfidf_matrix.pkl
```

It then maps a movie title to its corresponding index, retrieves its TF-IDF vector, calculates similarity scores against the movie matrix, sorts the results by similarity, and returns the highest-scoring movies. ([GitHub][3])

This allows the system to recommend movies that are mathematically similar to the selected movie based on the information represented in the TF-IDF data.

---

## 🎭 Genre Recommendations

In addition to TF-IDF recommendations, the backend provides genre-based recommendations.

For a selected TMDB movie, the application retrieves its details, identifies its first genre, and uses TMDB's movie discovery functionality to find popular movies from that genre. ([GitHub][3])

---

## 📁 Project Structure

```text
Movie-Recommendation-System/
│
├── .gitignore
├── .python-version
│
├── Movie-Recommendation-System.ipynb
│
├── app.py
├── main.py
│
├── movies_metadata.csv
│
├── df.pkl
├── indices.pkl
├── tfidf.pkl
├── tfidf_matrix.pkl
│
├── favicon.png
├── requirements.txt
├── runtime.txt
│
└── README.md
```

The repository currently contains the application, FastAPI backend, notebook, movie metadata CSV, serialized TF-IDF resources, favicon, dependency file, and runtime configuration. ([GitHub][4])

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```powershell
git clone https://github.com/athrv18/Movie-Recommendation-System.git
```

### 2. Enter the Project Directory

```powershell
cd Movie-Recommendation-System
```

### 3. Create a Virtual Environment

```powershell
python -m venv venv
```

### 4. Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

The FastAPI backend requires a TMDB API key.

Create a `.env` file in the project root:

```env
TMDB_API_KEY=your_tmdb_api_key
```

The backend loads `TMDB_API_KEY` using `python-dotenv` and requires it to be available when the API starts. ([GitHub][3])

**Do not commit your actual API key to GitHub.**

---

## ▶️ Running the Project

### Start the FastAPI Backend

```powershell
uvicorn main:app --reload
```

The FastAPI application provides endpoints for health checks, TMDB movie search, movie details, home categories, genre recommendations, and TF-IDF recommendations. ([GitHub][3])

### Start the Streamlit Frontend

Open another PowerShell terminal:

```powershell
streamlit run app.py
```

The Streamlit application is configured to communicate with the deployed FastAPI service through the `API_BASE` environment variable, with the current deployed API URL configured as its default. ([GitHub][1])

For local development, `API_BASE` can be configured to point to your local FastAPI server.

---

## 🎯 Usage

1. Start the FastAPI backend.
2. Start the Streamlit application.
3. Open the Streamlit URL in your browser.
4. Search for a movie by title.
5. Select a movie from the search results.
6. Explore its details.
7. View similar movies generated through TF-IDF recommendations.
8. Explore genre-based recommendations.
9. Browse categories such as trending, popular, top-rated, now-playing, and upcoming movies.

The application also allows users to choose the movie category displayed on the home feed and control the number of movies shown per row. ([GitHub][1])

---

## 🌐 Deployment

The project is structured as a Streamlit frontend communicating with a FastAPI backend.

The Streamlit application currently uses the deployed FastAPI service:

https://movie-recommendation-system-2wx1.onrender.com

The backend requires the `TMDB_API_KEY` environment variable for TMDB API access. ([GitHub][1])

For a Render deployment, configure the required environment variable in the Render service rather than committing the API key to the repository.

---

## 📸 Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Movie Search

![Movie Search](screenshots/search.png)

### Movie Recommendations

![Movie Recommendations](screenshots/recommendations.png)

> Add your actual screenshots to a `screenshots` folder and update the filenames if necessary.

---

## 🚀 Future Improvements

Potential improvements for future versions include:

* Personalized recommendations based on user history
* User accounts and saved movies
* Ratings and watchlists
* More advanced recommendation algorithms
* Improved recommendation ranking
* Additional movie filters
* Recommendation explanations
* Improved caching for external TMDB requests
* Expanded movie metadata and discovery options

---

## 👨‍💻 Author

**Atharva**

GitHub:
[https://github.com/athrv18](https://github.com/athrv18)

---

## 📌 Project Repository

[Movie Recommendation System — GitHub Repository](https://github.com/athrv18/Movie-Recommendation-System?utm_source=chatgpt.com)

---

## ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.

[1]: https://github.com/athrv18/Movie-Recommendation-System/blob/main/app.py "Movie-Recommendation-System/app.py at main · athrv18/Movie-Recommendation-System · GitHub"
[2]: https://github.com/athrv18/Movie-Recommendation-System/blob/main/requirements.txt "Movie-Recommendation-System/requirements.txt at main · athrv18/Movie-Recommendation-System · GitHub"
[3]: https://github.com/athrv18/Movie-Recommendation-System/blob/main/main.py "Movie-Recommendation-System/main.py at main · athrv18/Movie-Recommendation-System · GitHub"
[4]: https://github.com/athrv18/Movie-Recommendation-System "GitHub - athrv18/Movie-Recommendation-System · GitHub"
