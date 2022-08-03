from rest_framework.routers import DefaultRouter
from django.conf.urls import re_path

from .views import *

urlpatterns = [
    re_path(r'^projects/$', ProjectListAPIView.as_view()),
    re_path(r'^projects/(?P<pk>\d+)/$', ProjectDetailAPIView.as_view()),
    re_path(r'^prototypes/$', PrototypeListAPIView.as_view()),
    re_path(r'^prototypes/(?P<pk>\d+)/$', PrototypeDetailAPIView.as_view()),
    re_path(r'^umls/$', UMLListAPIView.as_view()),
    re_path(r'^umls/(?P<pk>\d+)/$', UMLDetailAPIView.as_view()),
    re_path(r'^documents/$', DocumentListAPIView.as_view()),
    re_path(r'^documents/(?P<pk>\d+)/$', DocumentDetailAPIView.as_view()),
]

# router = DefaultRouter()
# router.register(r'projects', ProjectModelViewSet)
# urlpatterns += router.urls
