from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import *

urlpatterns = [
    path(r'projects/', ProjectListAPIView.as_view()),
    path(r'projects/copy/', ProjectCopyAPIView.as_view()),
    path(r'projects/<int:pk>/', ProjectDetailAPIView.as_view()),
    path(r'projects/star/', ProjectStarListAPIView.as_view()),
    path(r'projects/star/post/', ProjectStarPostAPIView.as_view()),
    path(r'prototypes/', PrototypeListAPIView.as_view()),
    path(r'prototypes/info/', PrototypeInfoAPIView.as_view()),
    path(r'prototypes/users/', PrototypeUserAPIView.as_view()),
    path(r'prototypes/<int:pk>/', PrototypeDetailAPIView.as_view()),
    path(r'prototypes/projects/<int:pk>/', PrototypeByProjectAPIView.as_view()),
    path(r'prototypes/ImageUpload/', ImageUpload.as_view()),
    path(r'umls/', UMLListAPIView.as_view()),
    path(r'umls/<int:pk>/', UMLDetailAPIView.as_view()),
    path(r'documents/', DocumentListAPIView.as_view()),
    path(r'documents/<int:pk>/', DocumentDetailAPIView.as_view()),
    path(r'documents/FileConvertor/', FileConvertor.as_view()),
    path(r'documents/center/<int:pk>/', DocumentCenterAPIView.as_view()),
]

# router = DefaultRouter()
# router.register(r'projects', ProjectModelViewSet)
# urlpatterns += router.urls