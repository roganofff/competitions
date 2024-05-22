from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'competitions', views.competition_viewset)
router.register(r'sports', views.sport_viewset)
router.register(r'stages', views.stage_viewset)
router.register(r'competitionssports', views.competitionssports_viewset)

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('competitions/', views.competition_list_view.as_view(), name='competitions'),
    path('competition/', views.competition_view, name='competition'),
    path('sports/', views.sport_list_view.as_view(), name='sports'),
    path('sport/', views.sport_view, name='sport'),
    path('stages/', views.stage_list_view.as_view(), name='stages'),
    path('stage/', views.stage_view, name='stage'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('profile/', views.profile, name='profile'),
]