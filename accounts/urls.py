from django.urls import path
from . import views
from . import oauth

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('oauth/<str:provider>/', oauth.oauth_login_view, name='oauth_login'),
    path('oauth/<str:provider>/callback/', oauth.oauth_callback_view, name='oauth_callback'),
]

