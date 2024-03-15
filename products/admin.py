from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "sku",
        "gtin12",
        "price",
        "availability",
        "average_rating",
        "display_image_urls",  # Custom method to display image URLs as separate links
    )

    ordering = ('sku',)

    def display_image_urls(self, obj):
        image_urls = obj.image_url.strip('[]').replace("'", "").split(', ')
        return mark_safe('<br>'.join(['<a href="{0}">{0}</a>'.format(url) for url in image_urls]))

    display_image_urls.short_description = 'Image URLs'

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
