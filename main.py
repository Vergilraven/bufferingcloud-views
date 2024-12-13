
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import admin, user, cursor, stock


bufferingcloud_dashboard = FastAPI(
    title="BufferingCloud Dashboard",
    description="控制面板API文档",
    version="1.0.1"
)

# 配置CORS
bufferingcloud_dashboard.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@bufferingcloud_dashboard.get("/")
async def root():
    """根路径返回基本信息"""
    return {
        "message": "欢迎使用 BufferingCloud Dashboard API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# 注册路由
bufferingcloud_dashboard.include_router(admin.router, prefix="/api/admin", tags=["管理员接口"])
bufferingcloud_dashboard.include_router(user.router, prefix="/api/user", tags=["用户接口"])
bufferingcloud_dashboard.include_router(cursor.router, prefix="/api/cursor", tags=["Cursor API"])
bufferingcloud_dashboard.include_router(stock.router, prefix="/api/stock", tags=["股票数据"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(bufferingcloud_dashboard, host="127.0.0.1", port=8000)
