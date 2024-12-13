import requests
from typing import Dict, Any, Optional
import json


class CursorAPI:
    def __init__(self, api_key: str, base_url: str = "https://api.cursor.sh/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送 API 请求的通用方法"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败: {str(e)}")

    def create_completion(self, 
                         prompt: str,
                         model: str = "gpt-3.5-turbo",
                         max_tokens: int = 1000,
                         temperature: float = 0.7) -> Dict[str, Any]:
        """创建文本补全请求"""
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        return self._make_request("POST", "/chat/completions", data)

    def create_embedding(self, text: str, model: str = "text-embedding-ada-002") -> Dict[str, Any]:
        """创建文本嵌入"""
        data = {
            "model": model,
            "input": text
        }
        return self._make_request("POST", "/embeddings", data)

    def list_models(self) -> Dict[str, Any]:
        """获取可用模型列表"""
        return self._make_request("GET", "/models")

    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """获取特定模型的详细信息"""
        return self._make_request("GET", f"/models/{model_id}")
