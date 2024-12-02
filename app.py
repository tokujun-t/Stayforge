from fastapi import FastAPI
from starlette.middleware import Middleware

import settings
from api import router as api_router
from webhook.middleware import WebhooksMiddleware

middleware = [
    Middleware(WebhooksMiddleware)
]
app = FastAPI(
    title="Stayforge API",
    description="This is a basic API description.",
    version=settings.__version__,
    docs_url="/docs",
    middleware=middleware
)

app.include_router(api_router.router, prefix="/api")

if __name__ == '__main__':
    import json

    with open("openapi.json", "w") as f:
        api_spec = app.openapi()
        f.write(json.dumps(api_spec))
    exit(0)
