"""Search endpoints"""
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/")
async def search(q: str = Query(...), type: str = "products"):
    """Search products and content"""
    # TODO: Implement Meilisearch integration
    return {"results": []}

@router.get("/suggestions")
async def get_search_suggestions(q: str = Query(...)):
    """Get search suggestions"""
    # TODO: Implement autocomplete suggestions
    return {"suggestions": []}
