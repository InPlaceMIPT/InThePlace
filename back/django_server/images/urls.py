from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from images import views

router = routers.DefaultRouter()
router.register(r'set', views.ImageViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'', include(router.urls)),
    path('image/<int:image_id>', views.ImageView.as_view()),
    path('4set/ids/', views.get_images_set),
    path('4set/url/', views.get_images_in_one),
]
