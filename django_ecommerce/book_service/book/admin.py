from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'price', 'stock_quantity', 'is_available')
    list_filter = ('genre', 'binding', 'is_available')
    search_fields = ('title', 'author', 'isbn')
    readonly_fields = ('created_at', 'updated_at') 