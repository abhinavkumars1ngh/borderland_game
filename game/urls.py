from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('play/', views.player_view),
    path('submit/', views.submit_number),
    path('host/', views.host_view),
    path('choose/', views.choose_loser),
    path('reset/', views.reset_round),
]