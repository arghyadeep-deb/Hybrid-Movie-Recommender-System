from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import download_models


# Load Pickles
with open("model/content_sim.pkl", "rb") as f:
    content_similarity = pickle.load(f)

with open("model/cf_sim.pkl", "rb") as f:
    cf_similarity = pickle.load(f)

with open("model/metadata.pkl", "rb") as f:
    meta = pickle.load(f)

new = meta["new"]
movie_ids = meta["movie_ids"]
tmdb_to_cf = meta["tmdb_to_cf"]

# FastAPI app
app = FastAPI(title="Hybrid Movie Recommender API")

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "backend running 🚀"}

# Return just titles
@app.get("/movies")
def get_movies():
    titles = new["title"].dropna().tolist()
    return titles


# Hybrid recommendation logic
def hybrid_recommend(title, n=10, alpha=0.6):
    if title not in new['title'].values:
        return None

    idx = new[new['title'] == title].index[0]
    tmdb_id = int(new.iloc[idx]['id'])

    content_scores = content_similarity[idx]

    cf_idx = tmdb_to_cf.get(tmdb_id, -1)
    if cf_idx != -1:
        cf_scores = np.zeros(len(content_scores))
        cf_scores[new.index.isin(new[new['id'].isin(movie_ids)].index)] = \
            cf_similarity[cf_idx]
    else:
        cf_scores = np.zeros(len(content_scores))

    final_scores = alpha * content_scores + (1 - alpha) * cf_scores
    similar = np.argsort(final_scores)[::-1]
    similar = [i for i in similar if i != idx][:n]

    results = []
    for i in similar:
        results.append({
            "movie_id": int(new.iloc[i]['id']),
            "title": new.iloc[i]['title']
        })
    return results


@app.get("/recommend/{title}")
def recommend(title: str, n: int = 10):
    recs = hybrid_recommend(title, n)
    if recs is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"recommendations": recs}
