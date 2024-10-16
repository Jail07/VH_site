from django.urls import path
from . import views
from .views import profile, RegisterView

app_name = 'web'

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
