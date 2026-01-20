import os
import requests

MODEL_DIR = "model"
os.makedirs(MODEL_DIR, exist_ok=True)

FILES = {
    "cf_sim.pkl": "1FPWuKFbJ6Y-TOYixPo6VMDoliJg8vPYh",
    "content_sim.pkl": "1wlkznyMPB5nFkenEg2boXW0XEFEe_qA2",
    "metadata.pkl": "1NE5hk92lOJH5Lqdg7XgT2tWtRBubhwOy",
    "tfidf.pkl": "1HMl0cEw3_9hXVFkXhO-_lzG0xstY85pG",
}

def download_file(url, dest):
    if os.path.exists(dest):
        print(f"{dest} already exists. Skipping download.")
        return

    print(f"Downloading {dest}...")
    response = requests.get(url)
    response.raise_for_status()

    with open(dest, "wb") as f:
        f.write(response.content)

for filename, url in FILES.items():
    download_file(url, os.path.join(MODEL_DIR, filename))
