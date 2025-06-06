from django.db import models


class Extraction(models.Model):
    image = models.ImageField(upload_to='extraction-images/')
    extraction_id = models.CharField(max_length=255, blank=True, null=True)
    batch_id = models.CharField(max_length=255, blank=True, null=True)  
    merchant = models.ForeignKey(
        'Merchant', on_delete=models.CASCADE, blank=True, null=True)


class ExtractionItem(models.Model):
    extraction = models.ForeignKey('Extraction', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(blank=True, null=True)


class Merchant(models.Model):
    merchant_address = models.CharField(max_length=255, blank=True, null=True)
    merchant_name = models.CharField(max_length=255)
    merchant_tax_id = models.CharField(max_length=255, blank=True, null=True)


# class ImageUpload(models.Model):
#     image = models.ImageField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)


# class ExtractionResponse(models.Model):
#     status = models.CharField(max_length=100)
#     extractionId = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)


# class UploadResponse(models.Model):
#     # status = models.CharField(max_length=100)
#     extractionId = models.CharField(max_length=100)
#     batchId = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)


# class AddBatchResultModel(models.Model):
#     extraction_id = models.CharField(max_length=100)
#     batch_id = models.CharField(max_length=100)


# class Item(models.Model):
#     name = models.CharField(max_length=255)
#     quantity = models.CharField(max_length=255)
#     total_price = models.CharField(max_length=255)
#     unit_price = models.CharField(max_length=255)


# class Result(models.Model):
#     grand_total = models.DecimalField(max_digits=10, decimal_places=2)
#     items = models.ManyToManyField(Item)
#     merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
#     receipt_date = models.DateField()
#     receipt_id = models.CharField(max_length=100)
#     total_tax_amount = models.DecimalField(max_digits=10, decimal_places=2)


# class File(models.Model):
#     fileId = models.CharField(max_length=100)
#     fileName = models.CharField(max_length=255)
#     status = models.CharField(max_length=100)
#     result = models.OneToOneField(Result, on_delete=models.CASCADE)
#     url = models.CharField(max_length=2048)


# class Extraction(models.Model):
#     extractionId = models.CharField(max_length=255)
#     batchId = models.CharField(max_length=255)
#     files = models.ManyToManyField(File)


# class UploadedFile(models.Model):
#     files = models.FileField()
#     extractionId = models.CharField(max_length=255)
#     batchId = models.CharField(max_length=255)
