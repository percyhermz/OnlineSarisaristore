from django.urls import path, include
from accounts import views


app_name='accounts'
urlpatterns = [
    path('register/', views.register_account, name="register_account"),
    path('logout/', views.logout_account, name="logout"),
    path('login/', views.login_account, name='login'),
    path('profile/', views.profile_view, name='profile'),
]
