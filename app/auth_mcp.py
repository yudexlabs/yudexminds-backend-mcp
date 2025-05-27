from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.config import Config

BEARER_TOKEN: str = Config.BEARER_TOKEN_MCP

class BearerAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/mcp"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
            
            token = auth_header.replace("Bearer ", "")
            if token != BEARER_TOKEN:
                return JSONResponse(status_code=403, content={"detail": "Forbidden"})
        
        return await call_next(request)