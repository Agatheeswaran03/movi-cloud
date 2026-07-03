from fastapi import APIRouter, HTTPException, status, Depends
from models import UserCreate, UserLogin, UserResponse
from database import users_collection
from auth import hash_password, verify_password, create_access_token, get_current_user
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user account."""
    try:
        # Check for existing email
        existing_user = await users_collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

        # Hash password and store user
        user_doc = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hash_password(user_data.password),
        }

        result = await users_collection.insert_one(user_doc)

        return {
            "message": "Account created successfully",
            "user": {
                "id": str(result.inserted_id),
                "name": user_data.name,
                "email": user_data.email,
            },
        }
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": tb}
        )


@router.post("/login")
async def login(credentials: UserLogin):
    """Authenticate user and return JWT token."""
    user = await users_collection.find_one({"email": credentials.email})

    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token with user ID as subject
    token = create_access_token(data={"sub": str(user["_id"])})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
        },
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user's profile."""
    return UserResponse(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"],
    )
