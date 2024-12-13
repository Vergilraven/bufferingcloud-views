from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r'^\d{11}$')
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "phone": "17317655839",
                "is_active": True
            }
        }

class UserProfile(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None 

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class SystemSettings(BaseModel):
    systemName: str
    description: str
    smtpServer: str
    smtpPort: int
    emailFrom: str
    enableTwoFactor: bool
    enableSSL: bool 

class ModelBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    version: str
    type: str = "classification"
    framework: str = "pytorch"
    description: str = ""
    usage_guide: str = ""
    is_active: bool = True
    gpu_required: bool = False
    batch_processing: bool = False
    memory_requirement: int = 4

class ModelCreate(ModelBase):
    pass

class ModelResponse(ModelBase):
    id: int
    updated_at: str

    class Config:
        from_attributes = True 

class CompletionRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7

class EmbeddingRequest(BaseModel):
    text: str
    model: str = "text-embedding-ada-002" 