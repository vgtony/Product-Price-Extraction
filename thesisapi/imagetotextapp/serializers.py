from rest_framework import serializers
from .models import AddBatchResultModel, Extraction, File, Merchant, Result, ImageUpload, Item, ExtractionResponse, UploadResponse, UploadedFile


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('id', 'image', 'uploaded_at')


class ExtractionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractionResponse
        fields = ['status', 'created_at', 'extractionId']


class UploadResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadResponse
        fields = '__all__'


class AddBatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddBatchResultModel
        fields = ['extraction_id', 'batch_id']


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
        merchant_serializer = MerchantSerializer(data=merchant_data)
        if merchant_serializer.is_valid():
            merchant = merchant_serializer.save()
            result = Result.objects.create(merchant=merchant, **validated_data)
            for item_data in items_data:
                item = Item.objects.create(**item_data)
                result.items.add(item)
            return result
        else:
            raise serializers.ValidationError(merchant_serializer.errors)

    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')
    #     merchant_data = validated_data.pop('merchant')
    #     merchant = MerchantSerializer.create(
    #         MerchantSerializer(), validated_data=merchant_data)
    #     result = Result.objects.create(merchant=merchant, **validated_data)
    #     for item_data in items_data:
    #         item = Item.objects.create(**item_data)
    #         result.items.add(item)
    #     return result


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
            result_serializer = ResultSerializer(data=result_data)
            if result_serializer.is_valid():
                result = result_serializer.save()
                File.objects.create(
                    result=result, **file_data, extraction=extraction)
            return extraction

    # def create(self, validated_data):
    #     files_data = validated_data.pop('files')
    #     extraction = Extraction.objects.create(**validated_data)
    #     for file_data in files_data:
    #         result_data = file_data.pop('result')
    #         merchant_data = result_data.pop('merchant')
    #         items_data = result_data.pop('items')
    #         merchant = Merchant.objects.create(**merchant_data)
    #         result = Result.objects.create(merchant=merchant, **result_data)
    #         for item_data in items_data:
    #             item = Item.objects.create(**item_data)
    #             result.items.add(item)
    #         File.objects.create(result=result, **file_data,
    #                             extraction=extraction)

    #     return extraction


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'extractionId']
