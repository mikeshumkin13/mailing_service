from django.contrib import admin
from django.core.mail import send_mail
from django.contrib import messages as dj_messages

from .models import Mailing, MailingLog

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'status')
    list_filter = ('status',)
    search_fields = ('id',)
    filter_horizontal = ('recipients',)
    actions = ['send_mailing']

    @admin.action(description='Отправить выбранные рассылки')
    def send_mailing(self, request, queryset):
        for mailing in queryset:
            if mailing.status != 'completed':
                success_count = 0
                fail_count = 0

                for client in mailing.recipients.all():
                    try:
                        send_mail(
                            subject=mailing.message.subject,
                            message=mailing.message.body,
                            from_email='noreply@example.com',
                            recipient_list=[client.email],
                            fail_silently=False,
                        )
                        MailingLog.objects.create(
                            mailing=mailing,
                            status='success',
                            server_response='OK'
                        )
                        success_count += 1
                    except Exception as e:
                        MailingLog.objects.create(
                            mailing=mailing,
                            status='failed',
                            server_response=str(e)
                        )
                        fail_count += 1

                mailing.status = 'started'
                mailing.save()

                dj_messages.success(
                    request,
                    f'Рассылка {mailing.id}: {success_count} успешно, {fail_count} не удалось.'
                )

@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempted_at', 'status')
    list_filter = ('status',)
    search_fields = ('server_response',)

