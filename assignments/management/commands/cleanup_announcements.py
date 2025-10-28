from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from assignments.models import Announcement


class Command(BaseCommand):
    help = 'Delete announcements older than a specified number of hours (default: 24)'

    def add_arguments(self, parser):
        parser.add_argument('--hours', type=int, default=24, help='Age in hours to keep announcements')

    def handle(self, *args, **options):
        hours = options.get('hours', 24)
        cutoff = timezone.now() - timedelta(hours=hours)
        old_qs = Announcement.objects.filter(created_at__lt=cutoff)
        count = old_qs.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No old announcements to delete.'))
            return
        old_qs.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} announcements older than {hours} hours.'))
