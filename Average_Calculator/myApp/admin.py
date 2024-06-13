from django.contrib import admin
from . models import Numbers

# Register your models here.

class dis_Numbers(admin.ModelAdmin):
    list_display = ('id', 'value', 'created_at')

admin.site.register(Numbers,dis_Numbers)
