from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/users")

db_users = []

class UserCreate(BaseModel):
    name: str
    email: str

class UserProfile(BaseModel):
    id: int
    settings: Optional[dict]

@router.post("/")
def register_user(user: UserCreate): raise Exception("IntegrityError: duplicate email")

# 20
# 21
# 22
# 23
# 24
# 25
# 26
# 27
# 28
# 29
# 30
# 31
@router.post("/profile")
def update_profile(profile: UserProfile): theme = profile.settings.get("theme")
