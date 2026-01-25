# Hybrid Movie Recommender System
A hybrid recommender that combines collaborative filtering and content-based techniques to provide personalized movie recommendations.  
This repository demonstrates training, evaluating, and deploying a recommendation pipeline end-to-end using a Python ML stack. The system is designed to be deployed with a FastAPI backend for inference and a Streamlit frontend for exploration and demos.

---

---

## About the Project

This project demonstrates a practical hybrid recommender approach that blends:
- Collaborative Filtering (implicit/explicit feedback, matrix factorization or embeddings)
- Content-Based Filtering (movie metadata such as genres, tags, descriptions, cast/director features)

The goal is to benefit from both user–item interaction patterns and item attributes to improve recommendation relevance, mitigate cold-start problems, and offer diverse suggestions.

---

## Features

- Hybrid recommendation using collaborative + content-based signals  
- Matrix factorization / embedding-based models 
- Item feature engineering (genres, year, tags, text embeddings from descriptions)  
- Cold-start handling via content-based fallback  
- Ranker for re-ranking (popularity, diversity, filters)  
- Top-K recommendation endpoints for users and "similar items" queries  
- FastAPI backend for inference and model serving  
- Streamlit interactive frontend for demoing recommendations   
- Clean, modular project structure suitable for experimentation and production
---

## Tech Stack

- Language: Python     
- Backend: FastAPI + uvicorn  
- Frontend: Streamlit  
- Data & processing: pandas, NumPy, scikit-learn  
- Persistence & artifacts: pickle  
---

## Project Structure

```
Hybrid-Movie-Recommender-System/
│
├── backend/
│   └── api.py                  (FastAPI backend & endpoints)
│
├── frontend/
│   └── app.py                  (Streamlit demo UI)
│
├── models/
│   ├── best_model.pt           (Best trained model / weights)
│   ├── final_model.pt          (Final model checkpoint)
│   ├── item_features.pkl       (Serialized item feature matrix)
│   ├── user_encoder.pkl        (User id encoder)
│   └── item_encoder.pkl        (Item id encoder)
│
├── notebooks/
│   └── EDA_and_training.ipynb  (Exploratory analysis & training code)
│
├── src/
│   ├── data.py                 (data loaders, preprocessing)
│   ├── features.py             (feature engineering)
│   ├── models.py               (model architectures and wrappers)
│   ├── train.py                (training loop)
│   └── eval.py                 (evaluation metrics and scripts)
│
├── requirements.txt            (Project dependencies)
├── .env                       (Environment variables)
├── .gitignore
└── README.md
```

---

## How to Run the Project

### Step 1: Install dependencies
```
pip install -r requirements.txt
```

(Use a virtual environment such as venv or conda.)

---

### Step 2: Prepare data & artifacts
- Place raw dataset files (e.g., MovieLens CSVs) in `data/` or configure paths in `.env`.
- Run preprocessing and training scripts or download prebuilt artifacts into `models/`.

Example:
```
python src/data.py --input data/movielens/ --output processed/
python src/train.py --config configs/train.yaml
```

---

### Step 3: Start the FastAPI backend
```
cd backend
uvicorn api:app --reload
```

#### Backend URL
```
http://127.0.0.1:8000
```

#### Health Check
```
GET /health
```

#### Swagger / OpenAPI
```
http://127.0.0.1:8000/docs
```

---

### Step 4: Run the Streamlit frontend
```
cd frontend
streamlit run app.py
```

Open the Streamlit URL shown in the terminal (usually http://localhost:8501).

---

## API Endpoints

### GET /health
Checks whether the API and model artifacts are loaded successfully.

Response:
```json
{ "status": "ok", "model_loaded": true }
```

---

### POST /recommend
Return top-K recommendations for a user.

Request body:
```json
{
  "user_id": 123,
  "k": 10,
  "filter_seen": true
}
```

Response:
```json
{
  "user_id": 123,
  "recommendations": [
    {"item_id": 356, "score": 4.21, "title": "The Shawshank Redemption"},
    {"item_id": 12,  "score": 3.95, "title": "The Godfather"},
    ...
  ]
}
```

---

### POST /similar
Return items similar to a given item (content or embedding similarity).

Request:
```json
{
  "item_id": 356,
  "k": 5
}
```

Response:
```json
{
  "item_id": 356,
  "similar": [
    {"item_id": 590, "score": 0.91, "title": "The Green Mile"},
    ...
  ]
}
```

(Exact endpoints and payloads depend on backend implementation — check `backend/api.py` for details.)

---

## Model Evaluation

Common metrics used:
- RMSE / MAE for rating prediction tasks  
- Precision@K, Recall@K for top-K recommendation  
- NDCG@K for ranking quality  
- MAP@K for mean average precision

Example (illustrative):
- RMSE: 0.86  
- Precision@10: 0.28  
- Recall@10: 0.52  
- NDCG@10: 0.34

Use `src/eval.py` to compute metrics on validation/test splits.

---

## Dataset
This project is compatible with MovieLens datasets (100K, 1M, 10M) and other explicit/implicit feedback collections. Movie metadata (title, genres, tags, descriptions) are used for content features and cold-start strategies.
---

## Purpose
This repository is intended to:
- Illustrate hybrid recommender design patterns (CF + content)  
- Provide an end-to-end pipeline: data → model → API → UI  
- Offer a starting point for experimentation with ranking, personalization, and productionization  
- Be a portfolio piece demonstrating practical ML engineering for recommender systems

---

## Contributing

Contributions are welcome. Typical workflows:
- Fork the repository
- Create a feature branch
- Add tests / notebook examples for new features
- Open a PR describing the changes

Please follow code style in existing files and include a short description of what you changed.
