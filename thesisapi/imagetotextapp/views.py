from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ExtractionSerializer, ExtractionWebhook
from .models import Extraction, ExtractionItem
from .utils import send_image_to_api, update_extraction_data
import json

class ExtractionsViewSet(viewsets.ModelViewSet):
    queryset = Extraction.objects.all()
    serializer_class = ExtractionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            extraction = serializer.save()
            extraction_data = send_image_to_api(extraction)
            extraction.extraction_id = extraction_data.get('extractionId', None)
            extraction.batch_id = extraction_data.get('batchId', None)
            extraction.save()
            
            updated_extraction = update_extraction_data(extraction, extraction_data)
            
            serializer = self.get_serializer(updated_extraction)

            print('extraction', extraction)

            return Response(data=serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def webhook(self, request):
        """
        Update the results from the webhook data
        """
        print('webhook', request.data)
        result_string = request.data.get('result')
        result_list = json.loads(result_string)
        print('result_list', result_list)
        for result in result_list:
            status = result.get("status")
            if status == "processed":
                extraction_id = result.get("extractionId")
                batch_id = result.get("batchId")
                extraction = Extraction.objects.get(extraction_id=extraction_id, batch_id=batch_id)
                items = result['result']['items']
                for item in items:
                    ExtractionItem.objects.create(
                        extraction=extraction,
                        product_name=item['name'],
                        product_price=item['unit_price'],
                        quantity=item['quantity'],
                    )
                serializer = self.get_serializer(extraction)

                return Response(data=serializer.data, status=200)
                # Return whatever data is stored in your Extraction model
                return Response({
                    'extractionId': extraction.extractionId,
                    'status': extraction.status if hasattr(extraction, 'status') else 'unknown',
                    'results': extraction.results if hasattr(extraction, 'results') else None,
                    # Add any other fields you want to return
                })
        else:
            return Response(status=200)
