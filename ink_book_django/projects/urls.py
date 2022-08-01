from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^projects/$', ProjectListAPIView.as_view()),
    url(r'^projects/(?P<pk>\d+)/$', ProjectDetailAPIView.as_view()),
]

# router = DefaultRouter()
# router.register(r'projects', ProjectModelViewSet)
# urlpatterns += router.urls
