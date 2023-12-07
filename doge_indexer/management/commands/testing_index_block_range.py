import time

from django.core.management.base import BaseCommand, CommandParser

from doge_indexer.indexer import DogeIndexerClient


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--from-block", "-f", type=int)
        parser.add_argument("--to-block", "-t", type=int)

    def handle(self, *args, **options):
        if "from_block" not in options or "to_block" not in options:
            print("Please provide --from-block (-f) and --to-block (-t) parameters")
            return

        from_block = options["from_block"]
        to_block = options["to_block"]

        indexer = DogeIndexerClient()
        start = time.time()
        for block in range(int(from_block), int(to_block) + 1):
            block_start = time.time()
            indexer.process_block(block)
            print(f"Processed block {block} in: ", time.time() - block_start)

        print(f"Processed block range ({from_block} - {to_block}) including in: ", time.time() - start)
