from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import UserMessage


class MessageListView(LoginRequiredMixin, ListView):
    model = UserMessage
    template_name = 'user_messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return UserMessage.objects.filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = UserMessage
    template_name = 'user_messages/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('user_messages:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = UserMessage
    template_name = 'user_messages/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('user_messages:message_list')

    def get_queryset(self):
        return UserMessage.objects.filter(user=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = UserMessage
    template_name = 'user_messages/message_confirm_delete.html'
    success_url = reverse_lazy('user_messages:message_list')

    def get_queryset(self):
        return UserMessage.objects.filter(user=self.request.user)


