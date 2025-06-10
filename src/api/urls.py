from ninja import NinjaAPI
from api.get_quiz.get_quiz_endpoint import router as get_quiz_router
from api.create_quiz.create_quiz_endpoint import router as create_quiz_router

api = NinjaAPI()
api.add_router("", get_quiz_router)
api.add_router("", create_quiz_router)
