from typing import Any

from django.db import models


class HexString32ByteField(models.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["max_length"] = 64
        super().__init__(*args, **kwargs)
