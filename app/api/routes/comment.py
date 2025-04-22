from fastapi import APIRouter, HTTPException
from app.services.CommentService import CommentService
from app.models.CommentModel import CommentModel

router = APIRouter(tags=["comment"])

@router.post("/comment")
async def create_comment(comment:CommentModel):
    try:
        is_created =  await CommentService.create_comment(comment)
        if is_created:
            return {"message": "Created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create comment data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/comment/post/{postId}")
async def get_all_comments(postId:str):
    try:
        return await CommentService.get_comments_post(postId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/comment/{commentId}")
async def get_comment_by_id(commentId:str):
    try:
        return await CommentService.get_comment_by_id(commentId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/comment/update")
async def update_comment(comment:CommentModel):
    try:
        is_updated = await CommentService.update_comment(comment)
        if is_updated:
            return {"message": "Updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update comment data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/comment/delete/{commentId}")
async def delete_comment(commentId:str):
    try:
        is_deleted = await CommentService.delete_comment(commentId)
        if is_deleted:
            return {"message": "Deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Comment not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))