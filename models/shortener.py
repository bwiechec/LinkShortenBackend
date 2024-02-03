from pydantic import BaseModel
from typing import Optional

class Shortener(BaseModel):    
    name: str
    url: str
    timestamp: str
    click_count: int

class OptionalShortener(BaseModel):   
    name: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[str] = None
    click_count: Optional[int] = None

def individual_serial(shortenUrl) -> dict:
    return {
        "id": str(shortenUrl["_id"]),
        "name": shortenUrl["name"],
        "url": shortenUrl["url"],
        "timestamp": shortenUrl["timestamp"],
        "click_count": shortenUrl["click_count"] if "click_count" in shortenUrl else 0
    }

def list_serial(shortenUrls) -> list:
    return [individual_serial(shortenUrl) for shortenUrl in shortenUrls]