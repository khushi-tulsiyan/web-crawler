import pytest
from app.crawler import extract_links, fetch_url, crawl
from fastapi.testclient import TestClient
import httpx
from app.crawler import app

# Test case for extracting links from a webpage
def test_extract_links():
    html = '''
    <a href="/about">About</a>
    <a href="http://external.com">External</a>
    '''
    base_url = "http://example.com"
    links = extract_links(base_url, html)
    assert "http://example.com/about" in links
    assert "http://external.com" not in links  # External links should be ignored

# Test case for fetching URL content (successful request)
@pytest.mark.asyncio
async def test_fetch_url_success():
    async with httpx.AsyncClient() as client:
        html = await fetch_url(client, "http://example.com")
        assert html is not None

# Test case for URL fetch failure (e.g., invalid URL)
@pytest.mark.asyncio
async def test_fetch_url_failure():
    async with httpx.AsyncClient() as client:
        html = await fetch_url(client, "http://invalid-url.com")
        assert html is None

# Test case for the crawling functionality
@pytest.mark.asyncio
async def test_crawl():
    async with httpx.AsyncClient() as client:
        visited = set()
        result = await crawl(client, "http://example.com", visited)
        assert "http://example.com" in result
        assert "http://example.com/about" in result  # Check if internal link is crawled
        assert len(result) > 0

# Test case for the FastAPI crawl endpoint
def test_crawl_endpoint():
    client = TestClient(app)
    response = client.post("/crawl", json={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "sitemap" in data
    assert "http://example.com" in data["sitemap"]
