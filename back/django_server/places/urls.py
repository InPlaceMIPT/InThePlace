from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from places import views

router = routers.DefaultRouter()
router.register(r'set', views.ProtoPlaceViewSet)
router.register(r'images', views.ImageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'', include(router.urls)),
    path('tags/<int:event_id>', views.TagsPlaceView.as_view()),
    path('info/<int:event_id>', views.InfoPlaceView.as_view()),
    path('info/list/', views.get_places_list),
]
