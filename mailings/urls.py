from django.urls import path
from .views import dashboard, MailingListView, MailingDetailView




app_name = 'mailings'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('list/', MailingListView.as_view(), name='mailing_list'),
    path('detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
]
