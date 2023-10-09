from rest_framework import serializers

from doge_indexer.models import DogeBlock


class DogeBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogeBlock
        fields = "__all__"
