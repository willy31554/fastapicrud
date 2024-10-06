from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Create FastAPI app with Swagger configuration
app = FastAPI(
    title="User Management API",
    description="This API allows you to perform CRUD operations on users.",
    version="1.0.0",
    docs_url="/docs",  # You can customize this URL if needed
    redoc_url="/redoc"  # Custom URL for ReDoc documentation
)

class User(BaseModel):
    id: int
    name: str
    email: str

users_db = []

# Create User
@app.post("/users/", response_model=User, tags=["Users"])
def create_user(user: User):
    users_db.append(user)
    return user

# Read User
@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def read_user(user_id: int):
    user = next((user for user in users_db if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update User
@app.put("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, updated_user: User):
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            users_db[idx] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# Delete User
@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int):
    global users_db
    users_db = [user for user in users_db if user.id != user_id]
    return {"message": "User deleted successfully"}
