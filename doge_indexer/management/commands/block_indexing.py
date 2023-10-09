from django.core.management.base import BaseCommand

from doge_indexer.indexer import DogeIndexerClient, DogeIndexerClientConfig

# txid = "19aeaa88859c04a333257f1119a77438ac08feec424c6ad3645a0679c8be9882"
# txid = "c8aafe466c59292f74dc9e3c8cc82fdda16edcf5d656d13b73219f96ff7b1d82"
txid = "95bf6eb2d5be272fc42b03cebc258a36e5f9c62079823208bd3026d6ed75e070"

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
        import time

        start = time.time()
        indexer.run()
        print("Full index in ", time.time() - start)
