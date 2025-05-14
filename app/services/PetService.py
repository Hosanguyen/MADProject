from app.models.PetModel import PetCreate, PetResponse
from app.core.database import Database
import uuid

class PetService:
    db = Database()
    table_name = "pet"
    
    @staticmethod
    async def create_pet(pet: PetCreate) -> PetResponse:
        conn = await PetService.db.acquire()
        pet_id = pet.id
        pet_create = (
            pet_id,
            pet.name,
            pet.breed_name,
            pet.gender,
            pet.birth_date,
            pet.color,
            pet.height,
            pet.weight,
            pet.image_url,
            pet.userid
        )
        
        try:
            async with conn.cursor() as cur:
                query = f"""
                INSERT INTO {PetService.table_name} (id, name, breed_name, gender, birth_date, color, height, weight, image_url, userid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                breed_name = VALUES(breed_name),
                gender = VALUES(gender),
                birth_date = VALUES(birth_date),
                color = VALUES(color),
                height = VALUES(height),
                weight = VALUES(weight),
                image_url = VALUES(image_url),
                userid = VALUES(userid);
                """
                await cur.execute(query, pet_create)
                await conn.commit()
                
                return PetResponse(
                    id=pet_id
                )
        except Exception as e:
            raise e
        finally:
            await PetService.db.release(conn)
        