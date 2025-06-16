from django.contrib import admin
from django.urls import path, include
from mailings.views import dashboard


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('mailings/', include('mailings.urls', namespace='mailings')),
]

