import mimetypes
from rest_framework import viewsets, generics
from .serializers import AddBatchResultSerializer, ExtractionSerializer, ItemSerializer, UploadResponseSerializer, ImageUploadSerializer, ExtractionResponseSerializer, UploadedFileSerializer
from .models import ImageUpload, ExtractionResponse, UploadResponse, Item, UploadedFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from dotenv import load_dotenv
import os


load_dotenv()


class ImageListView(generics.ListAPIView):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer


class CreateExtractionView(APIView):

    def post(self, request, *args, **kwargs):
        token = os.getenv('API_KEY')
        extraction_details = request.data.get("extractionDetails")

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not extraction_details:
            return Response({"error": "Extraction details are required"}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://api.extracta.ai/api/v1/createExtraction"
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}

        try:
            response = requests.post(
                url, json={"extractionDetails": extraction_details}, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            serializer = ExtractionResponseSerializer(data=response_data)
            if serializer.is_valid():
                serializer.save()
                extractionId = serializer.validated_data['extractionId']
                upload_files_view = UploadFilesView()
                response_final = upload_files_view.post(
                    request, extractionId=extractionId)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UploadFilesView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = UploadedFileSerializer(data=request.data)

        token = os.getenv('API_KEY')

        if serializer.is_valid():
            extraction_id = request.data.get("extractionId")
            batch_id = request.data.get("batchId")
            files = request.FILES.getlist("files")
            print('files', files)

            serializer.save()
            print('serializer', serializer.data)
            # files = serializer.data['files']

            if not token:
                return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

            if not extraction_id:
                return Response({"error": "Extraction ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            if not files:
                return Response({"error": "No files were submitted"}, status=status.HTTP_400_BAD_REQUEST)

            url = "https://api.extracta.ai/api/v1/uploadFiles"
            headers = {
                # "Content-Type": "multipart/form-data",
                "Authorization": f"Bearer {token}"
            }

            file_streams = [
                (
                    "files",
                    (
                        file.name,
                        file,
                        file.content_type
                    ),
                )
                for file in files
            ]

            print('file_streams', file_streams)

            for file in files:
                file.seek(0)

            payload = {
                "extractionId": extraction_id,
            }
            if batch_id is not None:
                payload["batchId"] = batch_id

            try:
                response = requests.post(
                    url, files=file_streams, data=payload, headers=headers)
                response.raise_for_status()
                print('response', response)

                response_data = response.json()

                print('response_data', response_data)

                # UploadResponse.objects.create(
                #     # status=response_data["status"],
                #     extraction_id=response_data["extractionId"],
                #     batch_id=response_data.get("batchId")
                # )

                return Response(response_data, status=status.HTTP_201_CREATED)
            except requests.RequestException as e:
                # Handle other requests exceptions
                print(f"Failed to upload files: {e}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Handle other possible exceptions
                print(f"An unexpected error occurred: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateExtractionModelViewSet (viewsets.ModelViewSet):
    queryset = ExtractionResponse.objects.all()
    serializer_class = ExtractionResponseSerializer


class UploadFilesModelViewSet(viewsets.ModelViewSet):
    queryset = UploadResponse.objects.all()
    serializer_class = UploadResponseSerializer


class AddBatchResult(APIView):

    def post(self, request, *args, **kwargs):
        serializer = AddBatchResultSerializer(data=request.data)
        token = os.getenv('API_KEY')
        if serializer.is_valid():

            serializer.save()

            headers = {
                'Content-Type': 'application/json',

                # 'Authorization': request.headers.get('Authorization')
                'Authorization': f"Bearer {token}"


            }
            # print(headers)
            # print(os.environ.get('API_KEY'))

            payload = {
                'extractionId': serializer.validated_data['extraction_id'],
                'batchId':  serializer.validated_data['batch_id']
            }
            url = "https://api.extracta.ai/api/v1/getBatchResults"
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            # print(response_data)
            serializerFinal = ExtractionSerializer(data=response_data)
            if serializerFinal.is_valid():

                serializerFinal.save()
                items = Item.objects.all()
                serializerItems = ItemSerializer(items, many=True)
                response_data['items'] = serializerItems.data
                print("auto einai to response_data", response_data)

                # response_data = {
                #     "extractionId": serializerFinal.validated_data['extractionId'],
                #     "batchId": serializerFinal.validated_data['batchId'],
                #     "files": serializerFinal.validated_data['files'],
                #     # "items": all_items
                #
                print("auto einai to Final", serializerFinal.validated_data)

                return Response(response_data, status=status.HTTP_201_CREATED)
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


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
