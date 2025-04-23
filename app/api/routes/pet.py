from fastapi import APIRouter, HTTPException, Request
from app.services.PetService import PetService
from app.models.PetModel import PetCreate, PetResponse


router = APIRouter(tags=["pet"])

@router.post("/pet/create")
async def create_pet(pet: dict) -> PetResponse:
    try:
        pet_create = PetCreate(**pet)
        pet_response = await PetService.create_pet(pet_create)
        return pet_response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))