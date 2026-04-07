# LMS Bootcamp Project

This is a fullstack Learning Management System (LMS) built with:

* **Frontend:** React (Vite) + Shadcn UI (JSX)
* **Backend:** Django + Django REST Framework (DRF)

---

## Project Structure

```
project-root/
├── backend/   # Django API
├── frontend/  # React App (Vite + Shadcn)
```

---

## Clone the Repository

```bash
git clone https://github.com/Wepply-Stack/lms-bootcamp-project.git
cd lms-bootcamp-project
```

---

## Branching Strategy

Each team member should work on their own branch.

### 🔹 Frontend Developers

```bash
git checkout -b frontend/your-name
```

### 🔹 Backend Developers

```bash
git checkout -b backend/your-name
```

### Example

```bash
git checkout -b frontend/john
git checkout -b backend/jane
```

---

## Prerequisites

Make sure you have installed:

* Node.js (**v18, v20 recommended** | v22 works with limitations)
* Python (3.10+)
* pip / virtualenv

---

# Backend Setup (Django DRF)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # MacOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install django djangorestframework django-cors-headers

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Backend runs on:
http://127.0.0.1:8000

---

# Frontend Setup (React + Vite + Shadcn)

## Step 1: Navigate to frontend

```bash
cd frontend
```

---

## Step 2: Install dependencies

```bash
npm install
```

---

## Step 3: Tailwind CSS Setup (IMPORTANT)

If not already configured:

```bash
npm install -D tailwindcss@3.4.1 postcss autoprefixer
npx tailwindcss init -p
```

### Update `tailwind.config.js`

```
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {} },
  plugins: [],
}
```

### Update `src/index.css`

```
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## Step 4: Setup Import Alias

Create `jsconfig.json`:

```
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

---

## Step 5: Initialize Shadcn UI

```bash
npx shadcn@latest init
```

---

## Step 6: Install Components

⚠️ If using Node v22:
**DO NOT use `--all`**

Instead install manually:

```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add form
npx shadcn@latest add table
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
```

---

## Step 7: Run Frontend

```bash
npm run dev
```

Frontend runs on:
http://localhost:5173

---

## Connecting Frontend & Backend

Make sure Django allows CORS in `config/settings.py`:

```
CORS_ALLOW_ALL_ORIGINS = True
```

API base URL:

```
http://127.0.0.1:8000/
```

---

## Tech Stack

* React (Vite)
* Tailwind CSS
* Shadcn UI (Radix)
* Django
* Django REST Framework

---

## Notes

* Node v22 works but has limitations with some CLI tools
* Use Node v18/v20 for best compatibility
* Always install only needed components in Shadcn

---

## Basic Git Workflow

```bash
# Pull latest changes
git pull origin main

# Create your branch
git checkout -b frontend/your-name

# Add changes
git add .

# Commit
git commit -m "your message"

# Push branch
git push origin your-branch-name
```
