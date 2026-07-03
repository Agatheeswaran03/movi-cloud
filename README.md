# TaskFlow — Task Manager Application

A full-stack task management application with user authentication, CRUD operations, and a beautiful golden-themed UI.

## Tech Stack

- **Frontend:** React + Vite
- **Backend:** Python + FastAPI
- **Database:** MongoDB

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- MongoDB (running on `localhost:27017`)

### 1. Configure MongoDB
You can run MongoDB locally or use MongoDB Atlas.

- Local MongoDB:
  ```bash
  mongod
  ```
- MongoDB Atlas:
  1. Create a free Atlas cluster.
  2. Add a database user and whitelist your IP address.
  3. Copy the Atlas connection string and place it in `backend/.env`.

Example `backend/.env` values for Atlas:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster-url>/taskmanager?retryWrites=true&w=majority
DATABASE_NAME=taskmanager
JWT_SECRET=your-jwt-secret
JWT_EXPIRY_MINUTES=1440
```

If you need a template, use `backend/.env.example`.

### 2. Start the Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`

### 3. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
The app will be available at `http://localhost:5173`

## Features
- ✅ User registration & login with JWT authentication
- ✅ Create, read, update, delete tasks
- ✅ Task status tracking (Pending / In Progress / Completed)
- ✅ Due date management with overdue highlighting
- ✅ Filter tasks by status
- ✅ User isolation (each user sees only their own tasks)
- ✅ Responsive design for desktop & tablet
- ✅ Golden cream theme with smooth animations
