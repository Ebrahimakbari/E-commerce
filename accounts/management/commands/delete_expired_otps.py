from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from accounts.models import OtpEmail, OtpPhoneNumber


class Command(BaseCommand):
    help = 'delete all expired otps'
    def handle(self, *args, **options):
        expired_time = datetime.now() - timedelta(minutes=1)
        OtpEmail.objects.filter(created__lt=expired_time).delete()
        OtpPhoneNumber.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('all expired otps deleted.')
