from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from typing import List, Optional

from fastapi.responses import RedirectResponse
from config.database import collection
from models.shortener import OptionalShortener, Shortener, individual_serial, list_serial
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING

router = APIRouter()

#GET ALL
@router.get("/api/shorteners", tags=["Shorteners"])
async def get_shorten_urls(filter: OptionalShortener = Depends(), order_by: Optional[str] = None, order: Optional[str] = 'asc'):
    # Create a filter if filter_field and filter_value are provided
    query_filter = {k: v for k, v in filter.model_dump().items() if v is not None}

    # Determine the sort order
    sort_order = ASCENDING if order == 'asc' else DESCENDING

    # Query the collection with filter and sort
    shorteners = collection.find(query_filter).sort(order_by, sort_order) if order_by else collection.find(query_filter)

    return list_serial(shorteners)

#GET SINGLE 
@router.get("/api/shorteners/{id}", tags=["Shorteners"])
async def get_shorten_url(id: str):
    shorteners = collection.find({"_id": ObjectId(id)})
    return list_serial(shorteners)

#Post request method
@router.post("/api/shorteners", tags=["Shorteners"])
async def add_shorten_url(shorten_url: Shortener):
    try:
        shorten_url = dict(shorten_url)          
        name = shorten_url["name"]
        url = shorten_url["url"]
        timestamp = shorten_url["timestamp"]

        if "click_count" not in shorten_url:
            shorten_url["click_count"] = 0

        if (len(name) == 0 or len(url) == 0 or len(timestamp) == 0):
            raise HTTPException(status_code=400, detail="All fields must be filled")

        result = collection.insert_one(shorten_url)

        new_shorten_url = collection.find_one({"_id": result.inserted_id})
        return individual_serial(new_shorten_url)

    except HTTPException as e:
        raise HTTPException(status_code=500, detail=e.detail)
    
#patch request method
@router.patch("/api/shorteners/{id}", tags=["Shorteners"])
async def update_shorten_url(id: str, shorten_url: Shortener):
    try:
        shorten_url = dict(shorten_url)  
        shorten_url_non_null_fields = {k: v for k, v in shorten_url.items() if v is not None}
        
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": shorten_url_non_null_fields})

        if result.modified_count == 1:
            updated_shorten_url = collection.find_one({"_id": ObjectId(id)})
            return individual_serial(updated_shorten_url)

        else:
            raise HTTPException(status_code=404, detail="Shortener not found")

    except HTTPException as e:
        raise HTTPException(status_code=500, detail=e.detail)
    
#delete request method
@router.delete("/api/shorteners/{id}", tags=["Shorteners"])
async def delete_shorten_url(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 1:
            return Response(status_code=status.HTTP_200_OK)

        else:
            raise HTTPException(status_code=404, detail="Shortener not found")

    except HTTPException as e:
        raise HTTPException(status_code=500, detail=e.detail)
    
@router.get("/{id}", include_in_schema=False)
async def redirect_to_shorten_url(id: str):
    shorten_url = collection.find_one({"_id": ObjectId(id)})        
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"click_count": shorten_url["click_count"] + 1}})
    return RedirectResponse(url=shorten_url['url'], status_code=302)