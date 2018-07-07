from rest_framework import serializers, viewsets
from nebscan.models import NebBlock


class NebBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = NebBlock
        fields = ('height', 'hash', 'parent_hash', 'timestamp')


class NebBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NebBlock.objects.all()
    serializer_class = NebBlockSerializer
