from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from utils.cursor_api import CursorAPI
from models.schemas import CompletionRequest, EmbeddingRequest
import os

router = APIRouter()

# 从环境变量获取 API key
CURSOR_API_KEY = os.getenv("CURSOR_API_KEY")
cursor_api = CursorAPI(api_key=CURSOR_API_KEY)

@router.post("/completions")
async def create_completion(request: CompletionRequest) -> Dict[str, Any]:
    """创建文本补全"""
    try:
        response = cursor_api.create_completion(
            prompt=request.prompt,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embeddings")
async def create_embedding(request: EmbeddingRequest) -> Dict[str, Any]:
    """创建文本嵌入"""
    try:
        response = cursor_api.create_embedding(
            text=request.text,
            model=request.model
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_models() -> Dict[str, Any]:
    """获取可用模型列表"""
    try:
        return cursor_api.list_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}")
async def get_model_info(model_id: str) -> Dict[str, Any]:
    """获取特定模型信息"""
    try:
        return cursor_api.get_model_info(model_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 