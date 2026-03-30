# LMS Bootcamp Project

This is a fullstack Learning Management System (LMS) built with:

- **Frontend:** React (Vite) + Shadcn UI (JSX)
- **Backend:** Django + Django REST Framework (DRF)

---

## 📁 Project Structure

```
project-root/
├── backend/   # Django API
├── frontend/  # React App (Vite + Shadcn)
```

---

## 📥 Clone the Repository

```bash
git clone <your-repo-url>
cd lms-bootcamp-project
```

---

## 🌿 Branching Strategy

Each team member should work on their own branch.

### 🔹 Frontend Developers

```bash
git checkout -b frontend/your-name
```

### 🔹 Backend Developers

```bash
git checkout -b backend/your-name
```

### ✅ Example

```bash
git checkout -b frontend/john
git checkout -b backend/jane
```

---

## ⚙️ Prerequisites

Make sure you have installed:

- Node.js (v18 or v20 recommended)
- Python (3.10+)
- pip / virtualenv

---

# 🚀 Backend Setup (Django DRF)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework django-cors-headers

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Backend runs on:
👉 http://127.0.0.1:8000

---

# 🎨 Frontend Setup (React + Shadcn)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs on:
👉 http://localhost:5173

---

## 🔗 Connecting Frontend & Backend

Make sure Django allows CORS in `config/settings.py`:

```
CORS_ALLOW_ALL_ORIGINS = True
```

API base URL:

```
http://127.0.0.1:8000/api/
```

---

## 🧱 Tech Stack

- React (Vite)
- Shadcn UI (Radix + TailwindCSS)
- Django
- Django REST Framework

---

## 📌 Notes

- Use Node 18/20 for best compatibility with Shadcn
- Add components as needed:

  ```
  npx shadcn@latest add button
  ```

---

## 🔁 Basic Git Workflow

```bash
# Pull latest changes
git pull origin main

# Add changes
git add .

# Commit
git commit -m "your message"

# Push branch
git push origin your-branch-name
```

---

## 👨‍💻 Contributors

Bootcamp Team
