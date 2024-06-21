from django.db import models

# Create your models here.


class TextData(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ExtractionResponse(models.Model):
    status = models.CharField(max_length=100)
    extraction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class UploadResponse(models.Model):
    status = models.CharField(max_length=100)
    extraction_id = models.CharField(max_length=100)
    batch_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


# class Item(models.Model):
#     name = models.CharField(max_length=255)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)


class AddBatchResultModel(models.Model):
    extraction_id = models.CharField(max_length=100)
    batch_id = models.CharField(max_length=100)


# class BatchResultResponseModel(models.Model):
#     extractionId = models.CharField(max_length=255)
#     batchId = models.CharField(max_length=255)
#     fileId = models.CharField(max_length=255)
#     fileName = models.CharField(max_length=255)
#     status = models.CharField(max_length=255)
#     grand_total = models.DecimalField(
#         max_digits=10, decimal_places=2)
#     merchant_name = models.CharField(max_length=255)
#     merchant_address = models.TextField()
#     merchant_tax_id = models.CharField(max_length=255)
#     receipt_date = models.DateField()
#     receipt_id = models.CharField(max_length=255)
#     total_tax_amount = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0.00)
#     created_at = models.DateTimeField(auto_now_add=True)
#     items = models.ManyToManyField('Item', related_name='batch_results')


# class Item(models.Model):
#     receipt = models.ForeignKey(
#         BatchResultResponseModel, on_delete=models.CASCADE, default=0)
#     name = models.CharField(max_length=255)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)


# def __str__(self):
#     return f"Receipt ID: {self.receipt_id}"


# class Item(models.Model):
#     name = models.CharField(max_length=255)
#     quantity = models.CharField(max_length=255)
#     total_price = models.CharField(max_length=255)
#     unit_price = models.CharField(max_length=255)


# class Merchant(models.Model):
#     merchant_address = models.CharField(max_length=255)
#     merchant_name = models.CharField(max_length=255)
#     merchant_tax_id = models.CharField(max_length=255)


# class File(models.Model):
#     fileId = models.CharField(max_length=255)
#     fileName = models.CharField(max_length=255)
#     status = models.CharField(max_length=255)
#     grand_total = models.CharField(max_length=255)
#     items = models.ManyToManyField(Item)
#     merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
#     receipt_date = models.DateField()
#     receipt_id = models.CharField(max_length=255)
#     total_tax_amount = models.CharField(max_length=255)


class Merchant(models.Model):
    merchant_address = models.CharField(max_length=255)
    merchant_name = models.CharField(max_length=255)
    merchant_tax_id = models.CharField(max_length=255)


class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255)
    unit_price = models.CharField(max_length=255)


class Result(models.Model):
    grand_total = models.CharField(max_length=255)
    items = models.ManyToManyField(Item)


class File(models.Model):
    fileId = models.CharField(max_length=255)
    fileName = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    result = models.OneToOneField(Result, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    receipt_date = models.CharField(max_length=255)
    receipt_id = models.CharField(max_length=255)
    total_tax_amount = models.CharField(max_length=255)


class Extraction(models.Model):
    extractionId = models.CharField(max_length=255)
    batchId = models.CharField(max_length=255)
    files = models.ManyToManyField(File)
