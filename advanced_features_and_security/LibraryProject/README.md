Here’s a clean and professional **README documentation for Task 1 (Managing Permissions and Groups in Django)** that you can drop into your `advanced_features_and_security` repo under `bookshelf/README.md` or the project root.

---

# 📖 Task 1: Managing Permissions and Groups in Django

## 🎯 Objective

Enhance the security and functionality of the application by implementing **custom permissions** and **user groups** to control access to different parts of the system.

This allows us to assign roles such as *Editors*, *Viewers*, and *Admins* to users and enforce what actions each group can perform.

---

## ⚙️ Implementation Steps

### 1. Define Custom Permissions in Models

We extended the `Book` model with custom permissions in `bookshelf/models.py`:

```python
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

These permissions (`can_view`, `can_create`, `can_edit`, `can_delete`) are now available in the Django admin.

---

### 2. Create and Configure Groups

We created groups in the Django admin or via a script:

* **Editors** → Has `can_edit` and `can_create`
* **Viewers** → Has `can_view`
* **Admins** → Has all permissions

Example setup via Django shell:

```python
from django.contrib.auth.models import Group, Permission

editors, _ = Group.objects.get_or_create(name="Editors")
viewers, _ = Group.objects.get_or_create(name="Viewers")
admins, _ = Group.objects.get_or_create(name="Admins")

editors.permissions.add(
    Permission.objects.get(codename="can_edit"),
    Permission.objects.get(codename="can_create")
)
viewers.permissions.add(
    Permission.objects.get(codename="can_view")
)
admins.permissions.set(Permission.objects.filter(content_type__app_label="bookshelf"))
```

---

### 3. Enforce Permissions in Views

We applied permission checks using the `@permission_required` decorator in `bookshelf/views.py`.

Example:

```python
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    # Logic to edit book
    return render(request, "bookshelf/edit_book.html")

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    # Logic to view books
    return render(request, "bookshelf/book_list.html")
```

If a user does not have the required permission, Django will raise a `PermissionDenied` error (403).

---

### 4. Testing Permissions

We manually tested by:

1. Creating test users.
2. Assigning them to groups (`Editors`, `Viewers`, `Admins`).
3. Logging in and accessing restricted views.

✅ Editors could create and edit books.
✅ Viewers could only view books.
✅ Admins had full access.

---

## 📝 Summary

* **Custom Permissions** were added at the model level.
* **Groups** (`Editors`, `Viewers`, `Admins`) were configured to organize permissions.
* **Views** enforce permissions via decorators.
* **Documentation** ensures clarity for future maintenance.

