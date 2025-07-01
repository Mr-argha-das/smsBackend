from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_403_FORBIDDEN
from app.core.settings.dev import settings

class HostValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host")
        if host not in settings.allowed_hosts and "*" not in settings.allowed_hosts:
            return Response("Host not allowed", status_code=HTTP_403_FORBIDDEN)
        return await call_next(request)
