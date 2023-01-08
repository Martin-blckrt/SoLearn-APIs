# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import os
import json
import meilisearch
from .serializers import CommunesSerializer, CommunesSearchSerializer

meili_client = meilisearch.Client('http://127.0.0.1:7700')
MEILI_INDEX_NAME = 'communes'

DEP_PATH = os.path.join(os.getcwd(), "GeographyData", "departements")
SEARCH_PATH = os.path.join(os.getcwd(), "GeographyData", "search_communes", "communes_sorted_names.json")
SEARCH_HISTORY_LIMIT = 10


class DepartementsView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request):
        try:
            departements = os.listdir(DEP_PATH)
        except:
            return Response({'msg': 'Error while reading data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = []
        for dep in departements:
            file = open(os.path.join(DEP_PATH, dep, 'departement-' + dep + '.json'))
            data.append(json.load(file))
        return Response(json.dumps(data), status=status.HTTP_200_OK)


class CommunesView(APIView):

    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        serializer = CommunesSerializer(data=request.data)
        if serializer.is_valid():
            dep = serializer.validated_data['dep']
            try:
                file = open(os.path.join(DEP_PATH, dep, 'communes-' + dep + '.json'))
                data = json.load(file)
                return Response(data, status=status.HTTP_200_OK)
            except:
                return Response({'msg': 'Error while reading data, please verify the "dep" parameter'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SearchSuggestionsView(APIView):

    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        serializer = CommunesSearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            try:
                search_result = meili_client.index(MEILI_INDEX_NAME).search(query)
            except:
                return Response({'msg': 'Error with meilisearch server, it may not be started'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            response = search_result['hits']
            return Response(response[:SEARCH_HISTORY_LIMIT], status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)