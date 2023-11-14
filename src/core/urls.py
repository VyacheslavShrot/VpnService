from django.urls import path

from core.views import UserProfileView, RegisterView, BaseView, SiteCreateView, proxy_view

app_name = "core"

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('create_site/', SiteCreateView.as_view(), name='create_site'),
    path('<slug:user_site_name>/<path:routes_on_original_site>/', proxy_view, name='proxy_view'),
]
