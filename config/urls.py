from django.contrib import admin
from django.urls import path, include
from mailings.views import dashboard


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('mailings/', include('mailings.urls', namespace='mailings')),
    path('clients/', include('clients.urls')),
    path('messages/', include('user_messages.urls', namespace='user_messages')),
]

