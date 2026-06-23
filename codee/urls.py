from django.urls import path
from .views import *

urlpatterns = [
    path('student/',student_api.as_view()),
    path('student/<int:id>/',student_api.as_view()),
    path('student_list/',StudentListAPI.as_view()),
    path('school_api/',Schoolapi.as_view()),
    path('school_api/<int:id>/',Schoolapi.as_view()),
    path('teacher_api/<int:id>/',Teacherapi.as_view()),
    path('teacher_api/',Teacherapi.as_view()),
    
    

    
]
