from ninja import NinjaAPI
from app.quiz.get_quiz.get_quiz_endpoint import router as get_quiz_router
from app.quiz.create_quiz.create_quiz_endpoint import router as create_quiz_router

api = NinjaAPI()
api.add_router("", get_quiz_router)
api.add_router("", create_quiz_router)
