from django.contrib import admin
from .models import Post

class Userpostmodel(admin.ModelAdmin):
    list_display = ("receiver","company","date")
    search_fields = ("company","receiver")

admin.site.register(Post,Userpostmodel)
# Register your models here.
