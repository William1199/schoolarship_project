from django.contrib import admin
from .models import Articles, Category



# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Category)