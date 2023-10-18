
import time
from django.core.management.base import BaseCommand

from doge_indexer.indexer import DogeIndexerClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        indexer = DogeIndexerClient()
        indexer.run()

        # start = time.time()
        # # Biggest doge block
        # indexer.process_block(4738722)
        # print("Out: ", time.time() - start)
