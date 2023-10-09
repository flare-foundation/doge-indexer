from rest_framework.routers import SimpleRouter

from doge_indexer.views import DogeBlockViewSet, DogeTransactionViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"transaction", DogeTransactionViewSet, basename="transaction")
router.register(r"block", DogeBlockViewSet, basename="block")

urlpatterns = router.urls
