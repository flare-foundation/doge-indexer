from django.core.management.base import BaseCommand

from doge_indexer.indexer import DogeIndexerClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        indexer = DogeIndexerClient()

        # start = time.time()
        # # Biggest doge block
        # indexer.process_block(4738722)
        # print("Out: ", time.time() - start)

        index_blocks = [6319658]
        for block in index_blocks:
            print(f"indexing block {block}")

            indexer.process_block(block)
