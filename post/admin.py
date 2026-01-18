from django.contrib import admin
from .models import Post, PostAttachment, Comment
from django.utils.translation import gettext_lazy as _
# Register your models here.
# admin.site.register(Post)
# admin.site.register(PostAttachment)
# admin.site.register(Comment)

@admin.register(Post)
class CustomPostAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Автор'), {'fields': ('author',)}),
        (_('Основная информация поста (ru)'), {'fields': ('title_ru', 'Content_ru')}),
        (_('Основная информация поста (en)'), {'fields': ('title_en', 'Content_en')}),
        (_('Дополнительная информация поста'), {'fields': ('time_stamp', 'edited')}),
    )
    addfieldsets = (
        (_('Автор'), {'fields': ('author',)}),
        (_('Основная информация поста (ru)'), {'fields': ('title_ru', 'Content_ru')}),
        (_('Основная информация поста (en)'), {'fields': ('title_en', 'Content_en')}),
    )
    list_display = ('title', 'time_stamp', 'edited')
    search_fields = ('title', 'Content', 'author__username')
    ordering = ('title', 'time_stamp')

    def get_fieldsets(self, request,        obj = None):
        if obj:
            return self.fieldsets
        return self.addfieldsets
    
@admin.register(Comment)
class CustomCommentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Автор', {'fields': ('author',)}),
        ('Основная информация комментария', {'fields': ('Content',)}),
        ('Дополнительная информация комментария', {'fields': ('time_stamp', 'post',)}),
    )
    addfieldsets = (
        ('Автор', {'fields': ('author',)}),
        ('Основная информация комментария', {'fields': ('Content', 'post',)}),
    )
    list_display = ( 'time_stamp', 'Content', 'post',)
    search_fields = ( 'Content', 'author__username')
    ordering = ( 'time_stamp',)

    def get_fieldsets(self, request,        obj = None):
        if obj:
            return self.fieldsets
        return self.addfieldsets
    
@admin.register(PostAttachment)
class CustomPostAttachmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основная информация файла', {'fields': ('name', 'file' , 'post',)}),
    )
    addfieldsets = (
        ('Основная информация файла', {'fields': ( 'file' ,'post')}),
    )
    list_display = ('name' , 'file', 'post',)
    search_fields = ('name',)
    ordering = ('post', 'name')

    def get_fieldsets(self, request,        obj = None):
        if obj:
            return self.fieldsets
        return self.addfieldsets