from fastapi import APIRouter, HTTPException
from models.schemas import UserProfile

router = APIRouter()

@router.get("/profile")
async def get_profile():
    """获取用户个人信息"""
    return {
        "username": "test_user",
        "email": "test@example.com"
    }

@router.put("/profile")
async def update_profile(profile: UserProfile):
    """更新用户个人信息"""
    return profile 