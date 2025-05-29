from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("")
async def create_user():
	return {"user": "auth"}
