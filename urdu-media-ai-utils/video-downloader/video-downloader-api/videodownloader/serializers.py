from rest_framework import serializers # rest framework

class ItemSerializer(serializers.Serializer):
    """
        serializes the video data for database.
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
