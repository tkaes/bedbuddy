# --------------------------------------------
# Simple FastAPI authentication backend for BedBuddy
# --------------------------------------------
# This file creates two endpoints:
#   1. /auth/register  -> add a new user to MongoDB
#   2. /auth/login     -> verify username + password and return a JWT token
#
# We are using:
#   - FastAPI (web framework) (Tiangolo, 2025)
#   - Motor (async MongoDB driver) (MongoDB Inc., 2025)
#   - Passlib (for password hashing) (The Passlib Project, 2024)
#   - python-jose (for JWT tokens) (Davis, 2024)
#   - dotenv (to load secrets from .env variable) (PypA, 2025)
# 
# ----------------------------
# Imports and setup
# ----------------------------
# FastAPI is the asynchronous web framework used for defining REST endpoints (Tiangolo, 2025)
from fastapi import FastAPI, HTTPException
# Pydantic provides type validation for incoming request bodies (Tiangolo, 2025)
from pydantic import BaseModel
# Motor is the asynchronous MongoDB driver maintained by MongoDB Inc.(MongoDB Inc., 2025)
from motor.motor_asyncio import AsyncIOMotorClient
# Load environment variables from the .env configuration file (PyPA, 2025).
from dotenv import load_dotenv
# For accessing environment variable (Python Software Foundation, 2025)
import os

# Import the helper functions from security.py (Davis, 2024; The Passlib Project, 2024)
from security import hash_password, verify_password, create_access_token

# Load environment variables (.env should be in the same folder)(PyPA, 2024)
load_dotenv()

# Create the FastAPI app (Tiangolo, 2025)
app = FastAPI(title="BedBuddy Auth API")

# Connect to MongoDB Atlas (MongoDB Inc., 2025)
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Motor connects asynchronously, so we can use "await" when calling it
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users = db["users"]  # collection where we store user data


# ----------------------------
# Define what kind of data we expect from the user
# ----------------------------
class UserCreds(BaseModel):
    '''
    Defines the shape of the data coming in the request:
    - username: str
    - password: str
    (Tiangolo, 2025)
    '''
    username: str
    password: str

# ----------------------------
# Endpoint: Register
# ----------------------------
@app.post("/auth/register", status_code=201)
async def register(body: UserCreds):
    """
    Create a new user account (Tiangolo, 2025; MongoDB Inc., 2025).
    Steps:
      1. Check if username already exists in MongoDB.
      2. Hash the password with bcrypt (The Passlib Project, 2024).
      3. Save to MongoDB.
    """
    existing_user = await users.find_one({"username": body.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(body.password) # Secure bcrypt hash
    await users.insert_one({
        "username": body.username,
        "password_hash": hashed_pw
    })
    return {"msg": "User registered successfully"}


# ----------------------------
# Endpoint: Login
# ----------------------------
@app.post("/auth/login")
async def login(body: UserCreds):
    """
    Log in an existing user (Tiangolo, 2025).
    Steps:
      1. Find the user in the database (MongoDB Inc., 2025).
      2. Verify password using bcrypt 9The Passlib Project, 2024).
      3. If correct, create and return a JWT token (Davis, 2024).
    """
    user = await users.find_one({"username": body.username})

    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(body.username)
    return {"access_token": token, "token_type": "bearer"}


# ----------------------------
# How to test
# ----------------------------
"""
1. Run the API server:
   uvicorn auth_api:app --reload

2. In your browser, open:
   http://127.0.0.1:8000/docs

3. You'll see an automatic API tester.
   - Try POST /auth/register  →  create new user
   - Try POST /auth/login     →  log in and receive JWT token
"""
# References:
# Davis, M. P. (2024). python-jose: JWT library for Python
#       [Software repository]. GitHub. https://github.com/mpdavis/python-jose
# MongoDB Inc. (2025). Motor: Asynchronous Python driver for MongoDB
#       [Documentation]. https://motor.readthedocs.io/
# PyPA. (2025). python-dotenv* [Software package]. 
#       PyPI. https://pypi.org/project/python-dotenv/
# Python Software Foundation. (2025, October 29). os — 
#       Miscellaneous operating system interfaces. In Python 3.13 documentation*. 
#       https://docs.python.org/3/library/os.html
# The Passlib Project. (2024). Passlib: Password hashing framework for Python 
#       [Documentation]. https://passlib.readthedocs.io/
# Tiangolo, S. (2025). FastAPI documentation. FastAPI. 
#       https://fastapi.tiangolo.com/

