from django.core.management.base import BaseCommand

from nebscan.utils import Synchronizer


class Command(BaseCommand):
    help = 'Sync blockchain'

    def handle(self, *args, **options):
        synchronizer = Synchronizer()
        synchronizer.run()

        self.stdout.write(self.style.SUCCESS('Successfully synchronized'))
