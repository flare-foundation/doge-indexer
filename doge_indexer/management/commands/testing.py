from requests.auth import HTTPBasicAuth
from django.core.management.base import BaseCommand
from django.db import transaction

from doge_client.main import ClientInitConfig, DogeClient

import queue
from requests.sessions import Session
import threading

from pprint import pprint as pp
import time

from doge_indexer.models.transaction import DogeTransaction
from doge_indexer.models.transaction_outputs import TransactionInput, TransactionOutput

client_config: ClientInitConfig = {
    "url": "http://213.32.6.191:22555/",
    "username": "admin",
    "password": "b4987b3064d68a099d00d339fe72af92a09fa30b10306999be383d93c68ebfd5",
}


def new_session(config: ClientInitConfig):
    session = Session()
    session.auth = HTTPBasicAuth(client_config["username"], client_config["password"])
    return session


# txid = "19aeaa88859c04a333257f1119a77438ac08feec424c6ad3645a0679c8be9882"
# txid = "c8aafe466c59292f74dc9e3c8cc82fdda16edcf5d656d13b73219f96ff7b1d82"
txid = "95bf6eb2d5be272fc42b03cebc258a36e5f9c62079823208bd3026d6ed75e070"


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = DogeClient(client_config)
        session = new_session(client_config)

        tx = client.get_transaction(session, txid).json()

        pp(tx["result"])

        tr = DogeTransaction.object_from_node_response(tx["result"], 4018812, 1639407120)

        pp(tr)

        outputs = [TransactionOutput.object_from_node_response(vout, tr) for vout in tx["result"]["vout"]]

        print("outputs len: ",len(outputs))

        inputs = []

        for ini, inp in enumerate(tx["result"]["vin"]):
            new_tx = client.get_transaction(session, inp["txid"]).json()

            inputs.append(TransactionInput.object_from_node_response(ini, inp, new_tx["result"]["vout"][inp["vout"]], tr))

        print("inputs len: ",len(inputs))

        with transaction.atomic():
            tr.save()
            for output in outputs:
                output.save()
            for inp in inputs:
                inp.save()
