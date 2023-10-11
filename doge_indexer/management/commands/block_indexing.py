from django.core.management.base import BaseCommand

from doge_indexer.indexer import DogeIndexerClient, DogeIndexerClientConfig

client_config: DogeIndexerClientConfig = {
    "url": "http://213.32.6.191:22555/",
    "username": "admin",
    "password": "b4987b3064d68a099d00d339fe72af92a09fa30b10306999be383d93c68ebfd5",
    "indexer_poll_interval": 10,
    "number_of_block_confirmations": 60,
    "initial_block_height": 4913834,
    "number_of_workers": 10,
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        indexer = DogeIndexerClient(client_config)
        indexer.run()
