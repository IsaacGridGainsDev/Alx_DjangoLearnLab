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
# Post Management (CRUD)

Routes:
- GET  /posts/                -> PostListView
- GET  /posts/new/            -> PostCreateView (authenticated)
- GET  /posts/<pk>/           -> PostDetailView
- GET  /posts/<pk>/edit/      -> PostUpdateView (author only)
- POST /posts/<pk>/delete/    -> PostDeleteView (author only)

Permission rules:
- Create: authenticated users only
- Edit/Delete: only post author
- List/Detail: public

Notes:
- PostCreateView sets `author` automatically via `form_valid`.
- Use `LoginRequiredMixin` and `UserPassesTestMixin` to enforce access control.
# Comments Feature

- Model: `Comment` (post FK, author FK, content, created_at, updated_at).
- Create: submit comment on a post's detail page (POST to `/posts/<pk>/`).
- Edit: `GET/POST /comments/<pk>/edit/` (author only).
- Delete: `POST /comments/<pk>/delete/` (author only).
- Templates:
  - `blog/posts/post_detail.html` shows comments and comment form.
  - `blog/comments/comment_form.html` and `comment_confirm_delete.html`.
- Tests: `blog/tests/test_comments.py`
