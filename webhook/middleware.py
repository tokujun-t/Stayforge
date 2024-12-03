import asyncio

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from api.webhooks_manager.models import *
from settings import logger
from webhook import sender


class WebhooksMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Get response
            response = await call_next(request)

            # Capture response body
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # Log request and response details
            logger.debug(
                f'WEBHOOK MANAGER - "catch_path": {request.url.path}, "catch_method": {request.method.upper()}, "catch_status": {response.status_code}'
            )

            # Create a task for the worker coroutine
            asyncio.create_task(sender.worker(request=request, response=response))

        except Exception as e:
            logger.error(f"Error occurred in middleware: {str(e)}")
            return Response("Internal Server Error", status_code=500)

        # Return original response
        return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))