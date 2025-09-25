# 📌 Task 1 – Views Customization (Django REST Framework)

This task focuses on customizing views in **Django REST Framework (DRF)** to handle form submissions, data validation, permissions, and filtering.

---

## 🔑 Objectives
1. **Customize CreateView and UpdateView**  
   - Override `perform_create()` and `perform_update()` methods.  
   - Add validation and enforce business logic during object creation or update.  

2. **Integrate Additional Functionalities**  
   - Use **permission checks** to restrict access (e.g., only authenticated users can create/update).  
   - Implement **filters** to allow searching and ordering of results.  
   - Demonstrate DRF’s built-in features and optional custom logic.  

---

## 📂 Files Modified
- `views.py` → Added `AuthorViewSet` and `BookViewSet` with customizations.

---

## ⚙️ Implementation

### 1. **Custom Create & Update**
DRF provides hooks (`perform_create`, `perform_update`) for customizing save logic.  

```python
def perform_create(self, serializer):
    serializer.save()   # Here you can enforce extra rules
    print("Book is being created")

def perform_update(self, serializer):
    serializer.save()
    print("Book is being updated")
