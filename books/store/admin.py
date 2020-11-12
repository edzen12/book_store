from django.contrib import admin

from store.models import Book, UserBookRelation


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'author_name')
    search_fields = ('name', 'price', 'author_name')
    list_display_links = ('id', 'name')


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'like', 'in_bookmarks', 'rate')


admin.site.site_title = "Магазин книг"
admin.site.site_header = "Магазин книг"
