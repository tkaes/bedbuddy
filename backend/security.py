# --------------------------------------------
# Simple security utilities for BedBuddy Auth
# --------------------------------------------
# This file handles:
#   1. Password hashing (no storage of raw passwords
#   2. Password verification (bcrypt, checks login attempts)
#   3. JWT token creation for login sessions (so client knows they are logged in)
#
# It works together with auth_api.py
#
# Libraries used:
#   - Passlib (for secure password hashing)
#   - python-jose (for signing JWT tokens)
#   - dotenv (to load secrets like keys)
#
# ----------------------------
# Imports
# ----------------------------
from passlib.context import CryptContext      # handles hashing of passwords (The Passlib Project, 2024)
from jose import jwt                          # encodes/decodes JWT access tokens (Davis, 2024)
from datetime import datetime, timedelta      # For setting token expiration times (Python Software Foundation, 2025)
from dotenv import load_dotenv                # For loading secrets from .env file (PyPA, 2025)
import os                                     # For accessing environment variables (Python Software Foundation, 2025)

# ----------------------------
# Setup
# ----------------------------
# Load environment variables from the .env file (hides secrets from code) (PyPA, 2025)
load_dotenv()

# Using Argon2 instead of bcrypt for password hashing.
# Argon2 is the 2015 Password Hashing Competition winner (Biryukov et al., 2015)
# and provides stronger resistance to GPU-based brute-force attacks.
# This change also avoids bcrypt's 72-byte password length limit and backend version issues.
# It is still one of the 4 recoomended password hashing but also the newest one (The Passlib Project, 2024)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Read JWT settings from .env variable (Davis, 2024)
SECRET_KEY = os.getenv("JWT_SECRET")           # secret key used to sign tokens
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")# Default algorithm HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60              # Token valied for 1-hour

# ----------------------------
# Password functions
# ----------------------------
def hash_password(password: str) -> str:
    """
    Turn a plain password into a secure bycrupt hash (The Passlib Project, 2024)
    This is what we save in the database instead of the raw password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain password matches the saved bcrypt hash (The Passlib Project, 2024)
    Used when the user tries to log in.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------
# Token functions
# ----------------------------
def create_access_token(username: str) -> str:
    """
    Create a signed JWT token that (Davis, 2024) includes:
      - 'sub': username (subject of the token)
      - 'exp': expiration timestampt (Python Software Foundation, 2025)
    This token will be sent back to the Tkinter client so the user 
    stays logged in for an hour
    """
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire_time}
    # Uses secret + algorithm from .env (PyPA, 2025)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# References:
#     Biryukov, A., Dinu, D., & Khovratovich, D. (2015). 
#           Argon2: The memory-hard function for password hashing and proof-of-work applications. 
#           Password Hashing Competition. https://password-hashing.net
#     Davis, M. P. (2024). python-jose: JWT library for Python[Software repositiory].
#           GitHub. https://github.com/mpdavis/python-jose
#     The Passlib Project. (2024). Passlib: Password hashing framework for Python. 
#           https://passlib.readthedocs.io/
#     PyPA. (2025). python-dotenv [Software package]. PyPI. 
#           https://pypi.org/project/python-dotenv/
#     Python Software Foundation. (2025, October 29). datetime — Basic date and time types.
#           In Python 3.13 documentation. 
#           https://docs.python.org/3/library/datetime.html
#     