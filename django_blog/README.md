# Django Blog – User Authentication System

This project extends a basic Django blog by adding a **user authentication system**.  
Users can now register, log in, log out, and manage their profiles (with bio and profile photo).

---

## 🚀 Features

- **Registration** (`/register/`)
  - Custom registration form (`UserRegisterForm`) with email validation.
- **Login** (`/login/`) / **Logout** (`/logout/`)
  - Uses Django’s built-in authentication views with custom templates.
- **Profile management** (`/profile/`)
  - Edit username, email, first/last name, bio, and upload a profile photo.
- **Security**
  - CSRF protection in all forms.
  - Password hashing using Django’s secure built-in algorithms.
  - Profile view requires authentication (`@login_required`).
- **Signals**
  - Automatic profile creation when a new user registers.

---

## ⚙️ Setup Instructions

1. **Clone the repo** and create a virtual environment:

   ```bash
   git clone <your-repo-url>
   cd django_blog
   python -m venv venv
   source venv/bin/activate   # on Linux/Mac
   venv\Scripts\activate      # on Windows
