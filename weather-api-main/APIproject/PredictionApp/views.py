from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from .serializers import PredictionSerializer
from catboost import CatBoostRegressor
from django.utils import timezone
import os
from .input_weatherAPI import getOpenWeatherData, getSolcastData
from .parser import Parser

MODEL_FILE = "catboost_model.json"
MODEL_PATH = os.path.join(os.getcwd(), "models", "saved_models", MODEL_FILE)
CROSS_VAL = 10

class PredictionView(APIView):
    def post(self, request):
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            prediction_model = serializer.save()
            prediction_model.email = request.user.email
            model = CatBoostRegressor()
            try:
                model.load_model(MODEL_PATH, format='json')
            except:
               return Response({ "msg" : f"Error loading the model from {MODEL_PATH}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Weather API calls & format data to fit fearures of the model
            open_weather_data = getOpenWeatherData(prediction_model.latitude, prediction_model.longitude, save_txt=False)
            solcast_data = getSolcastData(prediction_model.latitude, prediction_model.longitude, save_txt=False)
            parser = Parser(open_weather_data, solcast_data, save=True, save_format="json", lat=prediction_model.latitude, lon=prediction_model.longitude)
            formatted_data = parser.transfom()
            # Run prediction
            try:
                prediction_model.date_exec = timezone.now
                predictions = model.predict(formatted_data)
            except:
                return Response({ "msg" : "Error running the model" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # Save and return results
            try:
                formatted_data['prediction'] = predictions
                prediction_model.data = formatted_data.to_json()
                prediction_model.is_predicted = True
                return Response({ "data" : {formatted_data.to_json()} }, status=status.HTTP_200_OK)
            except:
                return Response({ "msg" : "Error formatting the final result" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)