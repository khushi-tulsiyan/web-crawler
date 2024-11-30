# Web Crawler API

## Overview
The **Web Crawler API** is a Python-based application built using FastAPI. It provides endpoints to fetch, parse, and process web pages, enabling users to extract useful information such as metadata, links, and text content. The application is containerized using Docker, making it easy to deploy and manage. The crawler is restricted to a single domain, ensuring it only follows internal links.

## Features
- Fetch HTML content from specified URLs.
- Extract metadata, links, and plain text.
- API-first design for easy integration.
- Lightweight and fast with FastAPI.
- Rate-limited crawling to avoid overloading websites.
- Concurrency control to limit the number of requests being handled at once.
- Dockerized for easy deployment and scaling.
- Automated tests for crawling functionality.

---

## Requirements
- Python 3.10 or higher
- Docker and Docker Compose (if using containerized deployment)

---

## Installation

### Using Docker
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd web-crawler
   ```

2. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

3. Access the API at `http://localhost:8000`.

### Without Docker
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd web-crawler
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API at `http://localhost:8000`.

---

## API Endpoints
| Method | Endpoint    | Description                      |
|--------|-------------|----------------------------------|
| GET    | `/`         | Root endpoint for testing.      |
| POST   | `/crawl`    | Trigger web crawling logic.      |

### Example
To fetch the root response, use:
```bash
curl http://localhost:8000/
```

To trigger the crawler, use:
```bash
curl -X 'POST' \
  'http://localhost:8000/crawl' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "http://example.com"
}'
```

#### Response Example:
```json
{
    "sitemap": {
        "http://example.com": {
            "http://example.com/about": {},
            "http://example.com/contact": {
                "http://example.com/contact/form": {}
            }
        }
    }
}
```

---

## Key Features Added
### 1. **Rate Limiting**
   - To prevent overloading the target server, we introduced rate-limiting by adding a delay between requests. The crawler waits for a specified amount of time (`RATE_LIMIT = 1 second`) before sending another request.

### 2. **Concurrency Control**
   - The crawler limits the number of concurrent requests using an `asyncio.Semaphore` to prevent overwhelming the server with too many simultaneous requests.

### 3. **Automated Testing**
   - **Test Functions**: We added unit tests using **pytest** to validate core functionalities:
     - Extracting links from HTML content.
     - Crawling websites and generating a valid sitemap.
     - Handling invalid URLs and failed requests gracefully.
   - Tests ensure that the application behaves as expected under various conditions.

---

## File Structure
```
web-crawler/
├── app/
│   ├── crawler.py          # Crawler logic
│   ├── router.py             # FastAPI entry point
│   └── utils.py            # Helper functions
├── tests/                  # Test directory
│   └── test_crawler.py     # Tests for crawler logic
├── Dockerfile              # Docker container setup
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Future Enhancements
- **Parallel Crawling**: Add support for parallel crawling with better queue management to handle large websites.
- **Advanced Parsing**: Implement more advanced HTML parsing and the ability to filter specific tags.
- **Retry Logic**: Automatically retry failed requests to handle temporary server issues.

---

## Troubleshooting
### Common Errors
1. **ModuleNotFoundError: No module named 'requests'**
   - Ensure dependencies are installed by running:
     ```bash
     pip install -r requirements.txt
     ```
   - If using Docker, rebuild the container:
     ```bash
     docker-compose up --build
     ```

2. **404: Not Found**
   - Ensure the server is running and accessible at the correct endpoint (e.g., `/` or `/crawl`).

3. **Docker warnings**
   - The `version` attribute in `docker-compose.yml` is deprecated. Remove it or use a supported version format.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Updates Summary:
- **Rate limiting** and **concurrency control** have been added to ensure efficient and safe crawling.
- **Automated tests** have been implemented to verify core features such as crawling, link extraction, and error handling.
- **Dockerization** and **Kubernetes deployment** are supported for easy setup and scaling.

