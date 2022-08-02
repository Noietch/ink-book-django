from django.urls import path
from .views import *

urlpatterns = [
    path(r'info/', GroupList.as_view()),
    path(r'user-group/',UserGroup.as_view()),
    path(r'info/<int:pk>/', GroupDetail.as_view()),
    path(r'relation-info/', GroupsRelationsList.as_view()),
    path(r'encryption/', Encryption.as_view()),
    path(r'decrypt/', Decrypt.as_view()),
    path(r'member-list/<int:pk>/', MemberList.as_view()),
]