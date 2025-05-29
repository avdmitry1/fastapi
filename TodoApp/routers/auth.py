from fastapi import APIRouter

router_auth = APIRouter(prefix="/auth", tags=["Auth"])


@router_auth.post("")
async def create_user():
	return {"user": "auth"}
