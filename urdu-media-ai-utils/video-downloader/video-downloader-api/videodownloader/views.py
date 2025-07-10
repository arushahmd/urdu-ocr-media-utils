from django.shortcuts import render

# Create your views here.
import os
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import VideoDownloader  # Assuming the class is in video_downloader.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ItemSerializer

# Dummy data
ITEMS = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1"},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2"},
]

class ItemListView(APIView):
    """
    API view to retrieve and create items.
    """

    def get(self, request):
        return Response(ITEMS, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            new_item = serializer.validated_data
            new_item['id'] = len(ITEMS) + 1
            ITEMS.append(new_item)
            return Response(new_item, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDownloadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    # Define file input in Swagger
    file_param = openapi.Parameter(
        "file", in_=openapi.IN_FORM, description="Text file with YouTube video links", type=openapi.TYPE_FILE
    )

    @swagger_auto_schema(manual_parameters=[file_param], responses={200: "Video download initiated."})
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith(".txt"):
            return Response({"error": "Invalid file format. Only .txt files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Read the video links from the file
        video_links = file.read().decode("utf-8").splitlines()

        if not video_links:
            return Response({"error": "The file is empty or no valid links were found."}, status=status.HTTP_400_BAD_REQUEST)

        video_downloader = VideoDownloader()
        download_results = []

        # Process each video link
        for link in video_links:
            if link.strip():  # Skip empty lines
                result = video_downloader.download_video(link)
                download_results.append(result)

        return Response(download_results, status=status.HTTP_200_OK)

