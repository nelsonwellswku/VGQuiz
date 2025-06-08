from ninja import NinjaAPI
from app.quiz.api import router

api = NinjaAPI()
api.add_router("api/", router)
