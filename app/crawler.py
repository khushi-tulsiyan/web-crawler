import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import asyncio
from fastapi import FastAPI, HTTPException

app = FastAPI()



semaphore = asyncio.Semaphore(10)

@app.get("/")
async def root():
    return {"message": "Welcome to the Web Crawler API!"}

async def fetch_url(client, url):
    async with semaphore:
        try:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except httpx.RequestError:
            return None

def extract_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    base_domain = urlparse(base_url).netloc

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        joined_url = urljoin(base_url, href)
        parsed_url = urlparse(joined_url)

        
        if parsed_url.netloc == base_domain:
            links.add(joined_url.split("#")[0])  # Remove fragments

    return links

async def crawl(client, url, visited):
    if url in visited:
        return {}
    
    visited.add(url)
    html = await fetch_url(client, url)
    if not html:
        return {}
    
    links = extract_links(url, html)
    site_map = {url: {}}

    
    for link in links:
        site_map[url].update(await crawl(client, link, visited))
    
    return site_map

@app.post("/crawl")
async def crawl_url(payload: dict):
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    visited = set()
    async with httpx.AsyncClient() as client:
        sitemap = await crawl(client, url, visited)
    
    return {"sitemap": sitemap}
