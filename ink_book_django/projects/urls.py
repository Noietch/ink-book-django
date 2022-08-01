from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from .views import *

urlpatterns = [

]

router = DefaultRouter()
router.register(r'projects', ProjectModelViewSet)
urlpatterns += router.urls
