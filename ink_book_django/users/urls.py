from django.urls import path
from .views import *

urlpatterns = [
    path(r'info/', UserList.as_view()),
    path(r'info/<int:pk>/', UserDetail.as_view()),
    path(r'email-verification', EmailVerification.as_view()),
]