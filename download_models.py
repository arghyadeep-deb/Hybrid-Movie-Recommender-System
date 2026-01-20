import os
import gdown

MODEL_DIR = "model"
os.makedirs(MODEL_DIR, exist_ok=True)

FILES = {
    "cf_sim.pkl": "1FPWuKFbJ6Y-TOYixPo6VMDoliJg8vPYh",
    "content_sim.pkl": "1wlkznyMPB5nFkenEg2boXW0XEFEe_qA2",
    "metadata.pkl": "1NE5hk92lOJH5Lqdg7XgT2tWtRBubhwOy",
    "tfidf.pkl": "1HMl0cEw3_9hXVFkXhO-_lzG0xstY85pG",
}

def download(file_id, output_path):
    if os.path.exists(output_path):
        print(f"{output_path} already exists. Skipping.")
        return

    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Downloading {output_path}...")
    gdown.download(url, output_path, quiet=False, fuzzy=True)

for filename, file_id in FILES.items():
    download(file_id, os.path.join(MODEL_DIR, filename))
