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


class ExtractionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractionResponse
        fields = ['status', 'created_at', 'extraction_id']


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
