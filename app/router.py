from fastapi import APIRouter, HTTPException
from app.crawler import fetch_html, parse_html

router = APIRouter()

@router.get("/crawl")
def crawl(url: str):
    """
    API endpoint to fetch and parse a webpage.
    Example: /crawl?url=https://example.com
    """
    try:
       
        html_content = fetch_html(url)

        
        parsed_data = parse_html(html_content)

        return {"success": True, "data": parsed_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
