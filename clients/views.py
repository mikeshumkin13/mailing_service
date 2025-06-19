from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Client
from django.contrib.auth.mixins import LoginRequiredMixin


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        if self.request.user.is_manager:
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)



class ClientCreateView(CreateView):
    model = Client
    template_name = 'clients/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

