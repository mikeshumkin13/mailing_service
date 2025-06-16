from django.urls import path
from .views import dashboard, mailing_list_view, mailing_detail_view



app_name = 'mailings'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('list/', mailing_list_view, name='mailing_list'),
    path('detail/<int:pk>/', mailing_detail_view, name='mailing_detail'),
]
