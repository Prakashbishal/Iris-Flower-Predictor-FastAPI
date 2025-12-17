import logging

from fastapi import FastAPI

from app.config import settings
from app.model_loader import load_model
from app.routers import predict as predict_router
from app.routers import health as health_router
from app.services.wiki import build_session, WikiThumbnailService

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("iris-api")

def create_app() -> FastAPI:
    app = FastAPI(title="Iris Classifier", version="1.0.0")

    @app.on_event("startup")
    def _startup():
        app.state.model = load_model(settings.model_path)

        if settings.enable_wiki:
            session = build_session(settings.wiki_user_agent)
            app.state.wiki = WikiThumbnailService(
                session=session,
                timeout_sec=settings.wiki_timeout_sec,
                enabled=True,
            )
        else:
            app.state.wiki = None

        logger.info("Model loaded from %s", settings.model_path.resolve())
        logger.info("Wikipedia enabled: %s", settings.enable_wiki)

    app.include_router(health_router.router)
    app.include_router(predict_router.router)

    return app

app = create_app()
@app.get('/')
def home():
    return {'message': 'Iris Flower Predictor API'}

@app.get('/home')
def about():
    return {'message': 'Iris Flower Predictor API'}