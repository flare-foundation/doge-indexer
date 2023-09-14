from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import AFUser
from .serializers import AFUserSerializer


class UserViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_class = AFUserSerializer
    queryset = AFUser.objects.all()

    @action(methods=["GET"], detail=False)
    def me(self, request: Request) -> Response:
        return Response(self.get_serializer(request.user).data)
