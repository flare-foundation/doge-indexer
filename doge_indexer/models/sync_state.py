import time
from django.db import models

class TipSyncStateChoices(models.TextChoices):
    created = "created", "Created"
    syncing = "sync", "Syncing"
    up_to_date = "up_to_date", "Up to date"
    error = "error", "Error"

TIP_STATE_ID = 1

class TipSyncState(models.Model):
    sync_state = models.CharField(max_length=10, choices=TipSyncStateChoices.choices, db_column="syncState")
    latest_tip_height = models.PositiveIntegerField(db_column="latestTipHeight")
    latest_indexed_height = models.PositiveIntegerField(db_column="latestIndexedHeight")

    # timestamp of latest update
    timestamp = models.PositiveIntegerField(db_column="timestamp")


    def __str__(self) -> str:
        return f"Sync state: {self.sync_state} - latest tip height: {self.latest_tip_height} - latest indexed height: {self.latest_indexed_height}"
    
    @classmethod
    def get_tip_state(cls):
        if cls.objects.filter(pk=TIP_STATE_ID).exists():
            return cls.objects.get(pk=TIP_STATE_ID)
        else:
            return cls.objects.create(
                pk=TIP_STATE_ID,
                sync_state=TipSyncStateChoices.created,
                latest_tip_height=0,
                latest_indexed_height=0,
                timestamp = int(time.time())
            )
        