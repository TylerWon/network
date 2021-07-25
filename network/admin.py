from django.contrib import admin

from .models import User, Post, Like

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("timestamp",)
    list_display = ("poster", "content", "timestamp")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("liker", "post")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)