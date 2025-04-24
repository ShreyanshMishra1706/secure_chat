# from chat.views import register, user_login, user_logout
from django.urls import path
from . import views
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "chat"  # ✅ This is necessary to use 'chat:some_url_name'

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("room/<str:room_name>/", views.chat_room, name="chat_room"),
    path("users/", user_list, name="user_list"),  # User selection page
    path("about/", views.about, name="about"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)