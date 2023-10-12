from attrs import frozen


@frozen
class Config:
    NODE_RPC_URL: str
    AUTH_USERNAME: str
    AUTH_PASSWORD: str
    INDEXER_POLL_INTERVAL: int
    INITIAL_BLOCK_HEIGHT: int
    NUMBER_OF_BLOCK_CONFIRMATIONS: int
    NUMBER_OF_WORKERS: int
