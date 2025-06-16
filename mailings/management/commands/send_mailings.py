from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from mailings.models import Mailing, MailingLog

class Command(BaseCommand):
    help = 'Отправить активные рассылки'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        # Ищем рассылки, которые ещё не запущены, но уже должны отправляться
        mailings = Mailing.objects.filter(
            status='created',
            start_time__lte=now,
            end_time__gte=now,
        )

        for mailing in mailings:
            self.stdout.write(f"Запуск рассылки {mailing.id}")
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

            # Меняем статус на "started", чтобы не запускалась повторно
            mailing.status = 'started'
            mailing.save()

            self.stdout.write(self.style.SUCCESS(
                f'✔️ Успешно: {success}, ❌ Ошибки: {failed}'
            ))

