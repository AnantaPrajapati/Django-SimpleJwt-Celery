from django.contrib import admin
from .models import UserData, Notice, NoticeImage
from django.utils.html import format_html

class NoticeImageInline(admin.TabularInline):
    model = NoticeImage
    extra = 1
    fields =  ['image']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'display_image')
    inlines = [NoticeImageInline]
    def display_image(self, obj):
        notice_image = obj.images.first()
        if notice_image and notice_image.image:
            return format_html('<img src = "{}" width = "50" height = "50"/>', notice_image.image.url)
        return 'No image'
    
    display_image.short_description = 'Image'


admin.site.register(UserData)
admin.site.register(Notice, ServiceAdmin)
