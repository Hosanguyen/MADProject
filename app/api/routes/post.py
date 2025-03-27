from fastapi import APIRouter, HTTPException
from app.services.PostService import PostService
from app.models.PostModel import PostModel
from typing import List

router = APIRouter(tags=["post"])

@router.post("/post/add", response_model=PostModel)
async def create_post(post: PostModel):
    try:
        return await PostService.create_post(post)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
@router.get("/post/all", response_model=List[PostModel])
async def get_all_posts():
    try:
        return await PostService.getAll()
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    