from . import views
from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('verify_email/', views.UserViewSet.as_view({'post': 'verify_email'})),
    path('register/', views.UserViewSet.as_view({'post': 'create_user'})),
    path('login/', views.UserViewSet.as_view({'post': 'generate_token'})),
    path('auth/', include('djoser.urls')),
]
