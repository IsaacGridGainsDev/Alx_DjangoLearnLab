from django.contrib import admin
from .models import Author, Book, Library, Librarian
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
# admin.site.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Addotional Info", {'fields': ('date_of_birth', 'profile_photo')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Addotional Info", {'fields': ('date_of_birth', 'profile_photo')}),)

admin.site.register(CustomUser, CustomUserAdmin)
