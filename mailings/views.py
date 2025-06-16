from django.shortcuts import render
from clients.models import Client
from django.shortcuts import get_object_or_404
from mailings.models import Mailing, MailingLog
from django.contrib.auth.decorators import login_required

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

@login_required
def mailing_list_view(request):
    mailings = Mailing.objects.filter(user=request.user)
    return render(request, 'mailings/mailing_list.html', {'mailings': mailings})


@login_required
def mailing_detail_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, user=request.user)
    logs = MailingLog.objects.filter(mailing=mailing)

    context = {
        'mailing': mailing,
        'logs': logs,
    }
    return render(request, 'mailings/mailing_detail.html', context)



