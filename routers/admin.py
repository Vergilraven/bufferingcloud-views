from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from models.schemas import (UserCreate, UserResponse, LoginRequest, Token, 
                          SystemSettings, ModelCreate, ModelResponse)
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt
import uuid

router = APIRouter()

# 这里简化处理，实际应该从数据库验证
FAKE_USER = {"username": "admin", "password": "admin123"}
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 模拟数据库存储
USERS_DB = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "phone": "17317655839",
        "password": "admin123",
        "is_active": True
    }
]

# 模拟模型数据存储
MODELS_DB = [
    {
        "id": 1,
        "name": "示例模型",
        "version": "1.0.0",
        "type": "classification",
        "framework": "pytorch",
        "description": "这是一个示例模型",
        "usage_guide": "使用说明...",
        "is_active": True,
        "gpu_required": True,
        "batch_processing": True,
        "memory_requirement": 4,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """管理员登录"""
    if (login_data.username == FAKE_USER["username"] and 
        login_data.password == FAKE_USER["password"]):
        
        access_token = create_access_token(
            data={"sub": login_data.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=401,
        detail="用户名或密码错误"
    )

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/dashboard")
async def get_dashboard():
    """获取管理员仪表板数据"""
    return {
        "total_users": 100,
        "active_users": 80,
        "total_orders": 500
    }

@router.get("/users", response_model=List[UserResponse])
async def get_users():
    """获取所有用户列表"""
    return [
        {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "phone": user["phone"],
            "is_active": user["is_active"]
        }
        for user in USERS_DB
    ]

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """创建新用户"""
    try:
        # 检查用户名是否已存在
        if any(u["username"] == user.username for u in USERS_DB):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if any(u["email"] == user.email for u in USERS_DB):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被使用"
            )
        
        # 创建新用户数据
        new_user_data = UserResponse(
            id=len(USERS_DB) + 1,
            username=user.username,
            email=user.email,
            phone=user.phone,
            is_active=user.is_active
        )
        
        # 将用户数据存储到模拟数据库
        USERS_DB.append({
            "id": new_user_data.id,
            "username": new_user_data.username,
            "email": new_user_data.email,
            "phone": new_user_data.phone,
            "password": user.password,
            "is_active": new_user_data.is_active
        })
        
        return new_user_data
        
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate):
    """更新用户信息"""
    # 查找用户
    user_index = next(
        (index for (index, u) in enumerate(USERS_DB) if u["id"] == user_id),
        None
    )
    
    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查用户名是否与其他用户重复
    if any(u["username"] == user.username and u["id"] != user_id for u in USERS_DB):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否与其他用户重复
    if any(u["email"] == user.email and u["id"] != user_id for u in USERS_DB):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被使用"
        )
    
    # 更新用户信息
    USERS_DB[user_index].update({
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "is_active": user.is_active
    })
    
    if user.password:  # 如果提供了新密码
        USERS_DB[user_index]["password"] = user.password  # 实际应用中应该加密存储
    
    # 返回更新后的用户信息
    return {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "is_active": user.is_active
    }

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    # 这里应该实现删除用户的逻辑
    return {"message": "用户删除成功"}

@router.get("/settings")
async def get_settings():
    """获取系统设置"""
    return {
        "systemName": "BufferingCloud Dashboard",
        "description": "一个强大的管理系统",
        "smtpServer": "smtp.example.com",
        "smtpPort": 587,
        "emailFrom": "admin@example.com",
        "enableTwoFactor": False,
        "enableSSL": True
    }

@router.post("/settings")
async def update_settings(settings: SystemSettings):
    """更新系统设置"""
    # 这里应该实现保存设置到数据库的逻辑
    return settings 

# 模型管理相关路由
@router.get("/models", response_model=List[ModelResponse])
async def get_models():
    """获取所有模型列表"""
    return MODELS_DB

@router.post("/models", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(model: ModelCreate):
    """创建新模型"""
    # 检查模型名称是否已存在
    if any(m["name"] == model.name for m in MODELS_DB):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="模型名称已存在"
        )
    
    # 创建新模型
    new_model = {
        "id": len(MODELS_DB) + 1,
        **model.dict(),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    MODELS_DB.append(new_model)
    return new_model

@router.put("/models/{model_id}", response_model=ModelResponse)
async def update_model(model_id: int, model: ModelCreate):
    """更新模型信息"""
    # 查找模型
    model_index = next(
        (index for (index, m) in enumerate(MODELS_DB) if m["id"] == model_id),
        None
    )
    
    if model_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模型不存在"
        )
    
    # 检查模型名称是否与其他模型重复
    if any(m["name"] == model.name and m["id"] != model_id for m in MODELS_DB):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="模型名称已存在"
        )
    
    # 更新模型信息
    MODELS_DB[model_index].update({
        **model.dict(),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    return MODELS_DB[model_index]

@router.delete("/models/{model_id}")
async def delete_model(model_id: int):
    """删除模型"""
    # 查找并删除模型
    model_index = next(
        (index for (index, m) in enumerate(MODELS_DB) if m["id"] == model_id),
        None
    )
    
    if model_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模型不存在"
        )
    
    MODELS_DB.pop(model_index)
    return {"message": "模型删除成功"} 