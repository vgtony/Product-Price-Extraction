from django.contrib import admin
from .models import Extraction, ExtractionItem, Merchant

# Register your models here.


class ExtractionItemInline(admin.TabularInline):
    model = ExtractionItem


class ExtractionAdmin(admin.ModelAdmin):
    inlines = [
        ExtractionItemInline,
    ]


admin.site.register(Extraction, ExtractionAdmin)
admin.site.register(ExtractionItem)
admin.site.register(Merchant)
