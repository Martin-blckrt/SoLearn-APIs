from rest_framework import serializers

class CommunesSerializer(serializers.Serializer):
    dep = serializers.CharField(style={"input_type": "dep"}, required=True)

class CommunesSearchSerializer(serializers.Serializer):
    query = serializers.CharField(style={"input_type": "query"}, required=True)