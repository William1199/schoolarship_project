from django.contrib import admin
from .models import Articles, Category, Comment


# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Category)
admin.site.register(Comment)