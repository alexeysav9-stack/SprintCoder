from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exercise/<int:snippet_id>/', views.exercise, name='exercise'),
    path('exercise/random/', views.random_snippet, name='random_snippet'),
    path('api/save-attempt/', views.save_attempt, name='save_attempt'),
    path('result/<int:attempt_id>/', views.result, name='result'),
    path('history/', views.history, name='history'),
    path('profile/', views.profile, name='profile'),
]
