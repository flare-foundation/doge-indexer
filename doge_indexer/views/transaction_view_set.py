from rest_framework import mixins, viewsets

from doge_indexer.models import DogeTransaction
from doge_indexer.serializers import TransactionDetailSerializers


class DogeTransactionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    permission_classes = ()
    base_model = DogeTransaction
    serializer_class = TransactionDetailSerializers
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.base_model.objects.all()
        return queryset
