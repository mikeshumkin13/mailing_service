from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import Client
from django.urls import reverse_lazy


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        if self.request.user.is_manager:
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['full_name', 'email', 'comment']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

