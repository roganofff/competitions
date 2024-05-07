from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'competitions', views.CompetitionViewSet)
router.register(r'sports', views.SportViewSet)
router.register(r'stages', views.StageViewSet)

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
]