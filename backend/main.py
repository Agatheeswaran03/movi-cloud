from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import connect_db, close_db, create_indexes
from routes.auth_routes import router as auth_router
from routes.task_routes import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — runs on startup and shutdown."""
    # Startup: verify MongoDB connection and create indexes
    await connect_db()
    await create_indexes()
    print("[INFO] Connected to MongoDB and created indexes")
    yield
    # Shutdown: close the database connection
    close_db()
    print("[INFO] Application shutting down")


app = FastAPI(
    title="Task Manager API",
    description="A full-featured task management API with authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration — allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Task Manager API is running", "status": "healthy"}
