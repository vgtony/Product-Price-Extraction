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


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ['name', 'quantity', 'total_price', 'unit_price']


# class MerchantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Merchant
#         fields = ['merchant_address', 'merchant_name', 'merchant_tax_id']


# class ResultSerializer(serializers.ModelSerializer):
#     items = ItemSerializer(many=True)

#     class Meta:
#         model = Result
#         fields = ['grand_total', 'items']

# class ResultSerializer(serializers.ModelSerializer):
#     # Assuming 'items' is a reverse relation from Result to multiple Item instances
#     items = ItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Result
#         fields = '__all__'  # Adjust fields as necessary or explicitly include 'items'

#     def create(self, validated_data):
#         # Handle creation of Result object, excluding direct handling of 'items' here
#         # since 'items' are read-only in this context and should be handled separately
#         result = Result.objects.create(**validated_data)
#         return result


# class FileSerializer(serializers.ModelSerializer):
#     result = ResultSerializer()
#     # merchant = MerchantSerializer()

#     class Meta:
#         model = File
#         fields = ['fileId', 'fileName', 'status', 'result',
#                   ]

# class FileSerializer(serializers.ModelSerializer):
#     result = ResultSerializer()
#     merchant = MerchantSerializer()

#     class Meta:
#         model = File
#         fields = '__all__'

#     def create(self, validated_data):
#         result_data = validated_data.pop('result')
#         result_serializer = ResultSerializer(data=result_data)
#         if result_serializer.is_valid(raise_exception=True):
#             result = result_serializer.save()
#             file_instance = File.objects.create(
#                 result=result, **validated_data)
#             return file_instance
#         else:
#             raise serializers.ValidationError("Error with result data")

# class FileSerializer(serializers.ModelSerializer):
#     result = ResultSerializer()
#     merchant = MerchantSerializer(required=False)  # Making merchant optional

#     class Meta:
#         model = File
#         fields = '__all__'

#     def create(self, validated_data):
#         result_data = validated_data.pop('result')
#         # Handle merchant being optional
#         merchant_data = validated_data.pop('merchant', None)
#         result_serializer = ResultSerializer(data=result_data)
#         if result_serializer.is_valid(raise_exception=True):
#             result = result_serializer.save()
#             if merchant_data:
#                 merchant_serializer = MerchantSerializer(data=merchant_data)
#                 if merchant_serializer.is_valid(raise_exception=True):
#                     merchant = merchant_serializer.save()
#                     validated_data['merchant'] = merchant
#             file_instance = File.objects.create(
#                 result=result, **validated_data)
#             return file_instance
#         else:
#             raise serializers.ValidationError("Error with result data")


# class ExtractionSerializer(serializers.ModelSerializer):
#     files = FileSerializer(many=True)

#     class Meta:
#         model = Extraction
#         fields = ['extractionId', 'batchId', 'files']

# class ExtractionSerializer(serializers.ModelSerializer):
#     files = FileSerializer(many=True)

#     class Meta:
#         model = Extraction
#         fields = ['extractionId', 'batchId', 'files']

#     # def create(self, validated_data):
#     #     files_data = validated_data.pop('files')
#     #     extraction = Extraction.objects.create(**validated_data)
#     #     for file_data in files_data:
#     #         File.objects.create(extraction=extraction, **file_data)
#     #     return extraction

#     def create(self, validated_data):
#         files_data = validated_data.pop('files')
#         extraction = Extraction.objects.create(**validated_data)
#         for file_data in files_data:
#             # Extract and remove the result data from file_data
#             result_data = file_data.pop('result')
#             result_serializer = ResultSerializer(data=result_data)
#             if result_serializer.is_valid(raise_exception=True):
#                 # Create a Result instance using the ResultSerializer
#                 result = result_serializer.save()
#                 # Assign the created Result instance
#                 File.objects.create(extraction=extraction,
#                                     result=result, **file_data)
#         return extraction


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    merchant = MerchantSerializer()

    class Meta:
        model = Result
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        merchant_data = validated_data.pop('merchant')
        merchant = MerchantSerializer.create(
            MerchantSerializer(), validated_data=merchant_data)
        result = Result.objects.create(merchant=merchant, **validated_data)
        for item_data in items_data:
            item = Item.objects.create(**item_data)
            result.items.add(item)
        return result


class FileSerializer(serializers.ModelSerializer):
    result = ResultSerializer()

    class Meta:
        model = File
        fields = '__all__'


class ExtractionSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)

    class Meta:
        model = Extraction
        fields = '__all__'

    def create(self, validated_data):
        files_data = validated_data.pop('files')
        extraction = Extraction.objects.create(**validated_data)
        for file_data in files_data:
            result_data = file_data.pop('result')
            merchant_data = result_data.pop('merchant')
            items_data = result_data.pop('items')
            merchant = Merchant.objects.create(**merchant_data)
            result = Result.objects.create(merchant=merchant, **result_data)
            for item_data in items_data:
                item = Item.objects.create(**item_data)
                result.items.add(item)
            File.objects.create(result=result, **file_data,
                                extraction=extraction)

        return extraction
