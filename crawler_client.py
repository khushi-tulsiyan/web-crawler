import argparse
import requests

BASE_URL = "http://localhost:8000"

def crawl(url):
    response = requests.post(f"{BASE_URL}/crawl", json={"url": url})
    print(response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to crawl")
    args = parser.parse_args()
    crawl(args.url)
