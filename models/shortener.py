from pydantic import BaseModel
from typing import Optional

class Shortener(BaseModel):    
    name: str
    url: str
    timestamp: str

class OptionalShortener(BaseModel):   
    name: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[str] = None

def individual_serial(shortenUrl) -> dict:
    return {
        "id": str(shortenUrl["_id"]),
        "name": shortenUrl["name"],
        "url": shortenUrl["url"],
        "timestamp": shortenUrl["timestamp"],
    }

def list_serial(shortenUrls) -> list:
    return [individual_serial(shortenUrl) for shortenUrl in shortenUrls]