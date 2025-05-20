from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mailings.models import Mailing, MailingLog
from django.utils import timezone

class Command(BaseCommand):
    help = 'Send all active mailings manually'

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(
            status='created',
            start_time__lte=timezone.now(),
            end_time__gte=timezone.now()
        )

        for mailing in mailings:
            self.stdout.write(f'Запуск рассылки {mailing.id}')
            success = 0
            failed = 0

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
                    success += 1
                except Exception as e:
                    MailingLog.objects.create(
                        mailing=mailing,
                        status='failed',
                        server_response=str(e)
                    )
                    failed += 1

            mailing.status = 'started'
            mailing.save()

            self.stdout.write(f'Успешно: {success}, Ошибки: {failed}')
