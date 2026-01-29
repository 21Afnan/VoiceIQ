import json
import os
import time
import requests
import numpy as np
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

# -----------------------------
# Config
# -----------------------------
BASE_URL = "https://www.sunmarke.com"
MAX_DEPTH = 3
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Educational AI Research Bot)"
}

RELEVANCE_ANCHOR = """
Information about a school's admissions, eligibility criteria,
application process, academic programs, curriculum, fees,
student life, facilities, calendars, assessments, policies,
and daily school operations.
"""

# -----------------------------
# Utilities
# -----------------------------

def is_valid_url(url):
    if not url.startswith(BASE_URL):
        return False

    blocked = ["pdf", "login", "privacy", "terms", "cookie"]
    return not any(b in url.lower() for b in blocked)


def fetch_html(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.text


def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return " ".join(text.split())


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# -----------------------------
# Crawl Website
# -----------------------------

def crawl_site():
    visited = set()
    queue = [(BASE_URL, 0)]
    pages = []

    while queue:
        url, depth = queue.pop(0)

        if url in visited or depth > MAX_DEPTH:
            continue

        visited.add(url)
        print(f"Crawling: {url}")

        try:
            html = fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            text = clean_text(html)

            if len(text) > 300:
                pages.append({
                    "url": url,
                    "title": soup.title.string.strip() if soup.title else "",
                    "depth": depth,
                    "content": text
                })

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if is_valid_url(next_url):
                    queue.append((next_url, depth + 1))

            time.sleep(1)

        except Exception as e:
            print(f"Skipped {url}: {e}")

    return pages


# -----------------------------
# Semantic Filtering
# -----------------------------

def semantic_filter(pages, model):
    anchor_embedding = model.encode(RELEVANCE_ANCHOR)
    relevant_pages = []

    for page in pages:
        page_embedding = model.encode(page["content"][:2000])
        score = cosine_similarity(anchor_embedding, page_embedding)

        if score > 0.35:
            page["relevance_score"] = round(float(score), 3)
            relevant_pages.append(page)

    return relevant_pages


# -----------------------------
# Chunking
# -----------------------------

def chunk_text(text, chunk_size=900, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


def create_chunks(pages):
    all_chunks = []
    chunk_id = 0

    for page in pages:
        chunks = chunk_text(page["content"])

        for c in chunks:
            all_chunks.append({
                "chunk_id": chunk_id,
                "source_url": page["url"],
                "title": page["title"],
                "content": c
            })
            chunk_id += 1

    return all_chunks


# -----------------------------
# Embedding Generation
# -----------------------------

def generate_embeddings(chunks, model):
    embeddings = []

    for chunk in chunks:
        vector = model.encode(chunk["content"])
        embeddings.append({
            "chunk_id": chunk["chunk_id"],
            "embedding": vector.tolist(),
            "source_url": chunk["source_url"]
        })

    return embeddings


# -----------------------------
# Save JSON Files
# -----------------------------

def save_json(filename, data):
    with open(f"{OUTPUT_DIR}/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    print("🚀 Starting intelligent Sunmarke ingestion")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    raw_pages = crawl_site()
    print(f"Raw pages crawled: {len(raw_pages)}")

    relevant_pages = semantic_filter(raw_pages, model)
    print(f"Semantically relevant pages: {len(relevant_pages)}")

    chunks = create_chunks(relevant_pages)
    print(f"Chunks created: {len(chunks)}")

    embeddings = generate_embeddings(chunks, model)
    print(f"Embeddings generated: {len(embeddings)}")

    save_json("pages.json", relevant_pages)
    save_json("chunks.json", chunks)
    save_json("embeddings.json", embeddings)

    print("🎉 Ingestion completed successfully")
