from django.urls import path
from .views import (
    dashboard, MailingListView, MailingDetailView,
    MailingUpdateView, MailingDeleteView, MailingCreateView,
)




app_name = 'mailings'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('list/', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]
