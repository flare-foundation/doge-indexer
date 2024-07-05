from django.core.management.base import BaseCommand

from doge_indexer.indexer import DogeIndexerClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        indexer = DogeIndexerClient()
        indexer.run()
