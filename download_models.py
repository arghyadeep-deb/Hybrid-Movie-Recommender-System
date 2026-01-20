import os
import gdown

MODEL_DIR = "model"
os.makedirs(MODEL_DIR, exist_ok=True)

FILES = {
    "cf_sim.pkl": "1FPWuKFbJ6Y-TOYixPo6VMDoliJg8vPYh",
    "content_sim.pkl": "PASTE_CONTENT_SIM_FILE_ID",
    "metadata.pkl": "PASTE_METADATA_FILE_ID",
    "tfidf.pkl": "PASTE_TFIDF_FILE_ID",
}

def download(file_id, output_path):
    if os.path.exists(output_path):
        print(f"{output_path} already exists. Skipping.")
        return

    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Downloading {output_path}...")
    gdown.download(url, output_path, quiet=False)

for filename, file_id in FILES.items():
    download(file_id, os.path.join(MODEL_DIR, filename))
