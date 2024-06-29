from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import AddBatchResultSerializer, ExtractionSerializer, GroupSerializer, ItemSerializer, TextDataSerializer, UploadResponseSerializer, UserSerializer, ImageUploadSerializer, ExtractionResponseSerializer
from .models import TextData, ImageUpload, ExtractionResponse, UploadResponse, Item
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import requests
import mimetypes


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


class TextDataViewSet(viewsets.ModelViewSet):
    queryset = TextData.objects.all()  # Queryset for listing data (if applicable)
    serializer_class = TextDataSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ImageUploadView(generics.CreateAPIView):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageListView(generics.ListAPIView):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer


class CreateExtractionView(APIView):

    def post(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        extraction_details = request.data.get("extractionDetails")

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not extraction_details:
            return Response({"error": "Extraction details are required"}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://api.extracta.ai/api/v1/createExtraction"
        headers = {"Content-Type": "application/json",
                   "Authorization": token}

        try:
            response = requests.post(
                url, json={"extractionDetails": extraction_details}, headers=headers
            )
            response.raise_for_status()
            response_data = response.json()

            ExtractionResponse.objects.create(
                status=response_data["status"],
                created_at=response_data["createdAt"],
                extraction_id=response_data["extractionId"]
            )
            return Response(response_data, status=status.HTTP_201_CREATED)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UploadFilesView(APIView):

    def post(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        extraction_id = request.data.get("extractionId")
        # batch_id = request.data.get("batch_id")
        files = request.FILES.getlist("files")

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not extraction_id:
            return Response({"error": "Extraction ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not files:
            return Response({"error": "No files were submitted"}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://api.extracta.ai/api/v1/uploadFiles"
        headers = {
            "Authorization": token}

        file_streams = [
            (
                "files",
                (
                    file.name,
                    file,
                    file.content_type,
                ),
            )
            for file in files
        ]
        payload = {"extractionId": extraction_id}
        # if batch_id is not None:
        #     payload["batchId"] = batch_id

        try:
            response = requests.post(
                url, files=file_streams, data=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            UploadResponse.objects.create(
                status=response_data["status"],
                extraction_id=response_data["extractionId"],
                batch_id=response_data["batchId"]
            )
            return Response(response.json(), status=status.HTTP_201_CREATED)
        except requests.HTTPError as e:
            error_message = response.json() if response.content else str(e)
            return Response({"error": error_message}, status=response.status_code)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class GetBatchResultsView(APIView): auto ekana comment isws ksanaxrhsimopoihsw

#     def post(self, request, *args, **kwargs):

#         token = request.headers.get("Authorization")
#         extraction_id = request.data.get("extractionId")
#         batch_id = request.data.get("batchId")

#         serializer = BatchResultResponseSerializer(data=request.data)
#         url = "https://api.extracta.ai/api/v1/getBatchResults"
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': token
#         }
#         payload = {
#             'extractionId': extraction_id,
#             'batchId': batch_id
#         }

#         if serializer.is_valid():
#             response = requests.post(url, json=payload, headers=headers)
#             response.raise_for_status()
#             response_data = response.json()
#             print(response_data)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if not token:
        #     return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # if not extraction_id:
        #     return Response({"error": "Extraction ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # if not batch_id:
        #     return Response({"error": "Batch ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #
        #     batch_result_response = BatchResultResponse.objects.create(
        #         extraction_id=extraction_id,
        #         batch_id=batch_id,
        #         file_id=response_data['files'][0]['fileId'],
        #         file_name=response_data['files'][0]['fileName'],
        #         status=response_data['files'][0]['status'],
        #         grand_total=response_data['files'][0]['result']['grand_total'],
        #         merchant_address=response_data['files'][0]['result']['merchant']['merchant_address'],
        #         merchant_name=response_data['files'][0]['result']['merchant']['merchant_name'],
        #         merchant_tax_id=response_data['files'][0]['result']['merchant']['merchant_tax_id'],
        #         receipt_date=response_data['files'][0]['result']['receipt_date'],
        #         receipt_id=response_data['files'][0]['result']['receipt_id'],
        #         total_tax_amount=response_data['files'][0]['result']['total_tax_amount']

        #     )

        #     items_data = response_data['files'][0]['result']['items']
        #     for item_data in items_data:
        #         item = Item.objects.create(
        #             name=item_data['name'],
        #             quantity=item_data['quantity'],
        #             total_price=item_data['total_price'],
        #             unit_price=item_data['unit_price']
        #         )
        #         batch_result_response.items.add(item)
        #     return Response(response.json(), status=status.HTTP_200_OK)
        # except requests.HTTPError as e:
        #     error_message = response.json() if response.content else str(e)
        #     return Response({"error": error_message}, status=response.status_code)
        # except requests.RequestException as e:
        #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateExtractionModelViewSet (viewsets.ModelViewSet):
    queryset = ExtractionResponse.objects.all()
    serializer_class = ExtractionResponseSerializer


class UploadFilesModelViewSet(viewsets.ModelViewSet):
    queryset = UploadResponse.objects.all()
    serializer_class = UploadResponseSerializer


# class BatchResultModelViewSet(viewsets.ModelViewSet):
#     queryset = BatchResultResponse.objects.all()
#     serializer_class = BatchResultResponseSerializer


# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer


class AddBatchResult(APIView):

    def post(self, request, *args, **kwargs):
        serializer = AddBatchResultSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()

            headers = {
                'Content-Type': 'application/json',
                # θα το αλλαξω με environ variable
                'Authorization': request.headers.get('Authorization')

            }
            payload = {
                'extractionId': serializer.validated_data['extraction_id'],
                'batchId':  serializer.validated_data['batch_id']
            }
            url = "https://api.extracta.ai/api/v1/getBatchResults"
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print(response_data)
            serializerFinal = ExtractionSerializer(data=response_data)
            if serializerFinal.is_valid():
                print("auto einai to Final", serializerFinal.validated_data)

                serializerFinal.save()

                return Response(serializerFinal.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializerFinal.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemListView(APIView):
    """
    View to list all items in the database.
    """

    def get(self, request, format=None):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
