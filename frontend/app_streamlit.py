import streamlit as st
import requests

# CONFIG 
API_URL = "http://127.0.0.1:8000"     # Backend server
TMDB_API_KEY = "9d511dc3b71d25ee0893e19d862c497b"

st.set_page_config(
    page_title="Hybrid Movie Recommender",
    layout="wide"
)

st.title("🎬 Hybrid Movie Recommendation System")
st.write("Get personalized movie recommendations using hybrid filtering 🚀")

# FETCH MOVIE TITLES
@st.cache_data
def load_movie_list():
    try:
        res = requests.get(f"{API_URL}/movies")
        return res.json()
    except:
        return []

movies = load_movie_list()

if not movies:
    st.error("❌ Could not fetch movie list. Check backend.")
    st.stop()

# GET POSTER FROM TMDB
import requests
@st.cache_data(ttl=86400)   # cache 1 day
def fetch_movie_data(movie_id, title):
    # Default values
    movie = {
        "poster": None,
        "title": title,
        "genres": [],
        "rating": None,
        "year": None,
        "imdb_id": None,
        "trailer": None
    }

    #Try direct lookup using ID
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        data = requests.get(url, timeout=3).json()

        movie["poster"] = data.get("poster_path")
        if movie["poster"]:
            movie["poster"] = "https://image.tmdb.org/t/p/w500/" + movie["poster"]

        movie["genres"] = [g["name"] for g in data.get("genres", [])]
        movie["rating"] = data.get("vote_average")
        movie["year"] = data.get("release_date", "")[:4]
        movie["imdb_id"] = data.get("imdb_id")
    except:
        pass

    # If poster missing → Title search fallback
    if not movie["poster"]:
        try:
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
            search_data = requests.get(search_url, timeout=3).json()

            if search_data.get("results"):
                r = search_data["results"][0]
                if r.get("poster_path"):
                    movie["poster"] = "https://image.tmdb.org/t/p/w500/" + r["poster_path"]

                movie["year"] = r.get("release_date","")[:4]
                movie["rating"] = r.get("vote_average")
        except:
            pass

    # Fetch trailer using movie_id (if we know it)
    try:
        if movie.get("imdb_id") or movie_id:
            vids_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=en-US"
            vids = requests.get(vids_url, timeout=3).json().get("results", [])
            yt = next((v for v in vids if v["site"]=="YouTube" and v["type"]=="Trailer"), None)
            if yt:
                movie["trailer"] = f"https://www.youtube.com/watch?v={yt['key']}"
    except:
        pass

    return movie

# CALL HYBRID API 
def recommend(title, n=10):
    res = requests.get(f"{API_URL}/recommend/{title}?n={n}")
    if res.status_code != 200:
        return []
    return res.json().get("recommendations", [])

# UI
movie_choice = st.selectbox("🎯 Select a Movie:", movies)
num = st.slider("📌 Number of Recommendations", 5, 20, 10)

if st.button("Recommend 🍿"):
    with st.spinner("Fetching recommendations..."):
        recs = recommend(movie_choice, num)

    if len(recs) == 0:
        st.error("No recommendations found.")
    else:
        st.subheader("✨ Recommended Movies")
        cols = st.columns(5)   # Show 5 per row
        i = 0
        for rec in recs:
            col = cols[i % 5]
            with col:
                movie_details = fetch_movie_data(rec["movie_id"], rec["title"])

                # Title
                st.write(f"**{rec['title']}**")

                # Poster
                if movie_details["poster"]:
                    st.image(movie_details["poster"], width=200)
                else:
                    st.write("No poster available")

                # Metadata badges
                sub = ""
                if movie_details["year"]:
                    sub += f"📆 {movie_details['year']}  "
                if movie_details["rating"]:
                    sub += f"⭐ {round(movie_details['rating'],1)}  "
                if movie_details["genres"]:
                    sub += f"🎭 {movie_details['genres'][0]}"
                st.caption(sub)

                # IMDb link
                if movie_details["imdb_id"]:
                    imdb_url = f"https://www.imdb.com/title/{movie_details['imdb_id']}/"
                    st.markdown(f"[🎬 IMDb Page]({imdb_url})", unsafe_allow_html=True)

                # Trailer
                if movie_details["trailer"]:
                    st.markdown(f"[▶️ Watch Trailer]({movie_details['trailer']})", unsafe_allow_html=True)

            i += 1