from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import MailingForm
from django.contrib import messages

from clients.models import Client
from .models import Mailing, MailingLog


@login_required
def dashboard(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='started').count()
    unique_clients = Client.objects.count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    }
    return render(request, 'dashboard.html', context)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.is_manager:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_manager or obj.user == self.request.user:
            return obj
        raise Http404("Рассылка не найдена.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = MailingLog.objects.filter(mailing=self.object)
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ['status', 'start_time', 'end_time']  # при необходимости расширь
    template_name = 'mailings/mailing_form.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user and not request.user.is_manager:
            raise Http404("У вас нет доступа к этой рассылке.")
        return super().dispatch(request, *args, **kwargs)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user and not request.user.is_manager:
            raise Http404("У вас нет доступа к удалению.")
        return super().dispatch(request, *args, **kwargs)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Рассылка успешно создана.')
        return super().form_valid(form)


