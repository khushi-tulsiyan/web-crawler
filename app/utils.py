def validate_url(url: str) -> bool:
    """Validate if the given string is a proper URL."""
    import re
    regex = re.compile(
        r'^(http|https)://'  
        r'(\w+(\-\w+)*\.)+'  
        r'([a-zA-Z]{2,})'    
    )
    return re.match(regex, url) is not None

def format_response(data: dict) -> dict:
    """Format the parsed data into a user-friendly structure."""
    return {
        "metadata": data.get("metadata", {}),
        "links": list(set(data.get("links", []))),  # Remove duplicate links
        "text": data.get("text", "")[:1000]  # Limit text length
    }
