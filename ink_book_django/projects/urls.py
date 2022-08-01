from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^projects/$', ProjectListAPIView.as_view()),
    url(r'^projects/(?P<pk>\d+)/$', ProjectDetailAPIView.as_view()),
    url(r'^prototypes/$', PrototypeListAPIView.as_view()),
    url(r'^prototypes/(?P<pk>\d+)/$', PrototypeDetailAPIView.as_view()),
    url(r'^umls/$', UMLListAPIView.as_view()),
    url(r'^umls/(?P<pk>\d+)/$', UMLDetailAPIView.as_view()),
    url(r'^documents/$', DocumentListAPIView.as_view()),
    url(r'^documents/(?P<pk>\d+)/$', DocumentDetailAPIView.as_view()),
]

# router = DefaultRouter()
# router.register(r'projects', ProjectModelViewSet)
# urlpatterns += router.urls
