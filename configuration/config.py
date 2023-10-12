import os

from configuration.types import Config


def get_config() -> Config:
    # required env values
    node_rpc_url = os.environ["NODE_RPC_URL"]
    auth_username = os.environ["AUTH_USERNAME"]
    auth_password = os.environ["AUTH_PASSWORD"]

    # not required
    indexer_poll_interval = int(os.environ.get("INDEXER_POLL_INTERVAL", "10"))
    number_of_block_confirmations = int(os.environ.get("NUMBER_OF_BLOCK_CONFIRMATIONS", "60"))
    initial_block_height = int(os.environ.get("INITIAL_BLOCK_HEIGHT", "1"))
    number_of_workers = int(os.environ.get("NUMBER_OF_WORKERS", "10"))
    prune_keep_days = int(os.environ.get("PRUNE_KEEP_DAYS", "0"))
    prune_interval_seconds = int(os.environ.get("PRUNE_INTERVAL_SECONDS", "60"))

    return Config(
        NODE_RPC_URL=node_rpc_url,
        AUTH_USERNAME=auth_username,
        AUTH_PASSWORD=auth_password,
        INDEXER_POLL_INTERVAL=indexer_poll_interval,
        NUMBER_OF_BLOCK_CONFIRMATIONS=number_of_block_confirmations,
        INITIAL_BLOCK_HEIGHT=initial_block_height,
        NUMBER_OF_WORKERS=number_of_workers,
        PRUNE_KEEP_DAYS=prune_keep_days,
        PRUNE_INTERVAL_SECONDS=prune_interval_seconds,
    )


config = get_config()
