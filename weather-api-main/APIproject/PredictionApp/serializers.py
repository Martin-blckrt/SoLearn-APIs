from rest_framework import serializers
from .models import Prediction
from asyncio.windows_events import NULL

class PredictionSerializer(serializers.ModelSerializer):
    postal_code = serializers.CharField(style={"input_type": "postal_code"}, write_only=True)
    latitude = serializers.FloatField(style={"input_type": "latitude"}, write_only=True)
    longitude = serializers.FloatField(style={"input_type": "longitude"}, write_only=True)
    nb_days = serializers.IntegerField(style={"input_type": "nb_days"}, write_only=True)

    class Meta:
        model = Prediction
        fields = ['postal_code', 'latitude', 'longitude', 'nb_days']

    def save(self):
        
        prediction = Prediction(
            postal_code = self.validated_data['postal_code'],
            latitude = self.validated_data['latitude'],
            longitude = self.validated_data['longitude'],
            nb_days = self.validated_data['nb_days']
        )
        prediction.save()

        return prediction