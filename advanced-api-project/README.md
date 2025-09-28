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


# ✅ Advanced API Project – Task 4 Documentation

This README provides full documentation for **Task 4**, including **setup instructions**, **available endpoints**, **example queries** (filtering, searching, ordering), and **how to run tests**.

---

## 🚀 Setup Instructions

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/advanced-api-project

# 2️⃣ Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ Create superuser (optional, for admin panel)
python manage.py createsuperuser

# 6️⃣ Run the development server
python manage.py runserver
