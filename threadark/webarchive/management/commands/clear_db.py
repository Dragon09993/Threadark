from django.core.management.base import BaseCommand
from webarchive.models import Board, Thread, Message
# from webarchive.models import TwoFactorCode  # COMMENTED OUT - 2FA DISABLED

class Command(BaseCommand):
    help = 'Clear all data from the database'

    def add_arguments(self, parser):
        parser.add_argument('--confirm', action='store_true', help='Confirm you want to delete all data')

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(self.style.WARNING('Use --confirm to actually clear the database'))
            return

        self.stdout.write('Clearing database...')
        
        # Delete all data
        Message.objects.all().delete()
        Thread.objects.all().delete()
        Board.objects.all().delete()
        # TwoFactorCode.objects.all().delete()  # COMMENTED OUT - 2FA DISABLED
        
        self.stdout.write(self.style.SUCCESS('Database cleared successfully!'))