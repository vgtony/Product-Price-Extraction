from rest_framework import viewsets
from .serializers import ExtractionSerializer
from .models import Extraction
from rest_framework.response import Response
from .utils import send_image_to_api
from .utils import update_extraction_data


class ExtractionsViewSet(viewsets.ModelViewSet):
    queryset = Extraction.objects.all()
    serializer_class = ExtractionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            extraction = serializer.save()
            extraction_data = send_image_to_api(extraction)
            update_extraction_data(extraction, extraction_data)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
