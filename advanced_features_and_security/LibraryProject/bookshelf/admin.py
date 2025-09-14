from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
# Register your models here.



class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publication_year')
    list_filter = ('title', 'author')
    search_fields = ('title', 'author')
admin.site.register(Book)

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Addotional Info", {'fields': ('date_of_birth', 'profile_photo')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Addotional Info", {'fields': ('date_of_birth', 'profile_photo')}),)

admin.site.register(CustomUser, CustomUserAdmin)

editors, created = Group.objects.get_or_create(name='Editors')
viewers, created = Group.objects.get_or_create(name='Viewers')

editors.permissions.add(Permission.objects.get(codename='can_add_book'))
editors.permissions.add(Permission.objects.get(codename='can_change_book'))
editors.permissions.add(Permission.objects.get(codename='can_delete_book'))

viewers.permissions.add(Permission.objects.get(codename='can_view_book'))