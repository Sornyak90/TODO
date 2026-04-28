from fastapi import APIRouter


router = APIRouter(prefix="/db")

@router.post("/")
async def create_user():
    pass

@router.patch("/")
async def update_user():
    pass

@router.delete("/")
async def delete_user():
    pass