from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin

app = FastAPI()

@app.post("/crawl")
async def crawl(url: str):
    sitemap = {}
    visited = set()

    def crawl_recursive(base_url, current_url):
        if current_url in visited:
            return
        visited.add(current_url)
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, "html.parser")
            sitemap[current_url] = []
            for link in soup.find_all("a", href=True):
                full_url = urljoin(base_url, link["href"])
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    sitemap[current_url].append(full_url)
                    crawl_recursive(base_url, full_url)
        except:
            pass

    crawl_recursive(url, url)
    return sitemap
