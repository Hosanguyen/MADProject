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
    
@router.get("/post/{postId}")
async def get_post_by_id(postId:str):
    try:
        return await PostService.get_post_by_id(postId)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
@router.put("/post/update")
async def update_post(post: PostModel):
    try:
        return await PostService.update_post(post)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
@router.delete("/post/delete/{postId}")
async def delete_post(postId: str):
    try:
        is_deleted = await PostService.delete_post(postId)
        if is_deleted:
            return {"message": "Xóa bài viết thành công"}
        else:
            raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))