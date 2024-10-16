from .views import profile, RegisterView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'web'

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)