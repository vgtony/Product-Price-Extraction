from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import AddBatchResultModel, Extraction, File, Merchant, Result, TextData, ImageUpload, Item, ExtractionResponse, UploadResponse


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TextDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextData
        fields = ['url', 'text', 'created_at', 'updated_at']


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('id', 'image', 'uploaded_at')


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = '__all__'


class ExtractionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractionResponse
        fields = '__all__'


class UploadResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadResponse
        fields = '__all__'


# class BatchResultResponseSerializer(serializers.ModelSerializer):
#     items = ItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = BatchResultResponse
#         fields = '__all__'


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         # fields = ['name', 'quantity', 'total_price', 'unit_price']
#         fields = '__all__'


# class BatchResultResponseSerializer(serializers.ModelSerializer):
#     items = ItemSerializer(many=True)

#     class Meta:
#         model = BatchResultResponseModel
#         fields = '__all__'

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         batch_result_response = BatchResultResponseModel.objects.create(
#             **validated_data)
#         for item_data in items_data:
#             item = Item.objects.create(**item_data)
#             batch_result_response.items.add(set(item))
#         return batch_result_response

# class BatchResultResponseSerializer(serializers.ModelSerializer):
#     items = ItemSerializer(many=True)

#     class Meta:
#         model = BatchResultResponse
#         (
#             'extraction_id',  # Assuming this is not optional
#             'batch_id',        # Assuming this is not optional
#             'file_id',         # Assuming this is not optional
#             'file_name',
#             'status',
#             'grand_total',
#             'merchant_address',
#             'merchant_name',
#             'merchant_tax_id',
#             'receipt_date',
#             'receipt_id',
#             'total_tax_amount',
#             'items',
#         )

#     def create(self, validated_data):
#         data = validated_data.pop('data')
#         items_data = data.pop('items')
#         merchant_data = data.pop('merchant')
#         batch_result_response = BatchResultResponse.objects.create(
#             file_name=validated_data['file_name'],
#             grand_total=data['grand_total'],
#             receipt_date=data['receipt_date'],
#             receipt_id=data['receipt_id'],
#             total_tax_amount=data['total_tax_amount'],
#             merchant_address=merchant_data['merchant_address'],
#             merchant_name=merchant_data['merchant_name'],
#             merchant_tax_id=merchant_data['merchant_tax_id'],
#         )
#         for item_data in items_data:
#             item = Item.objects.create(**item_data)
#             batch_result_response.items.add(item)
#         return batch_result_response


class AddBatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddBatchResultModel
        fields = ['extraction_id', 'batch_id']


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ['name', 'quantity', 'total_price', 'unit_price']


# class MerchantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Merchant
#         fields = ['merchant_address', 'merchant_name', 'merchant_tax_id']


# class FileSerializer(serializers.ModelSerializer):
#     items = ItemSerializer(many=True)
#     merchant = MerchantSerializer()

#     class Meta:
#         model = File
#         fields = ['fileId', 'fileName', 'status', 'grand_total', 'items',
#                   'merchant', 'receipt_date', 'receipt_id', 'total_tax_amount']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'total_price', 'unit_price']


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['merchant_address', 'merchant_name', 'merchant_tax_id']


class ResultSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Result
        fields = ['grand_total', 'items']


class FileSerializer(serializers.ModelSerializer):
    result = ResultSerializer()
    # merchant = MerchantSerializer()

    class Meta:
        model = File
        fields = ['fileId', 'fileName', 'status', 'result',
                  ]


class ExtractionSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)

    class Meta:
        model = Extraction
        fields = ['extractionId', 'batchId', 'files']
