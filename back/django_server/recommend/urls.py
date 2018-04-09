from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from recommend import views


router = routers.DefaultRouter()
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'', include(router.urls)),
    path('byimageid/', views.recommend_by_images),
]
