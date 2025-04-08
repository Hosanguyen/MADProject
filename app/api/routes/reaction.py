from fastapi import APIRouter, HTTPException
from app.services.ReactionService import ReactionService
from app.models.ReactionModel import ReactionModel

router = APIRouter(tags=["reaction"])

@router.post("/reaction")
async def create_reaction(reaction: ReactionModel):
    try:
        is_created = await ReactionService.create_reaction(reaction)
        if is_created:
            return {"message": "Created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create reaction data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/reaction/post/{postId}")
async def get_all_reactions(postId: str):
    try:
        return await ReactionService.get_reactions_by_postid(postId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/reaction/{reactionId}")
async def get_reaction_by_id(reactionId: str):
    try:
        return await ReactionService.get_reaction_by_id(reactionId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/reaction/update")
async def update_reaction(reaction: ReactionModel):
    try:
        is_updated = await ReactionService.update_reaction(reaction)
        if is_updated:
            return {"message": "Updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update reaction data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/reaction/delete/{reactionId}")
async def delete_reaction(reactionId: str):
    try:
        is_deleted = await ReactionService.delete_reaction(reactionId)
        if is_deleted:
            return {"message": "Deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Reaction not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))