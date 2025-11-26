# Database Config handles retrieval of sensitive information from environment file
# And creation of Mongo client

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 1. Find the bedbuddy root folder
PROJECT_ROOT= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Build the full path to backend/.env
ENV_PATH= os.path.join(PROJECT_ROOT, "backend", ".env")

# 3. Load variables from that .env file
load_dotenv(ENV_PATH)

# 4. MongoDB Atlas connection string and name of database
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# 5. Instantiation of client
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

# References:
#
# OWASP Foundation. (2023). OWASP cheat sheet series: Secrets management.
#   https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
#
# Python Software Foundation. (2025). dotenv — loading environment variables.
#   https://docs.python.org/3/library/os.html
#
# ZohourianShahzadi, Z. (2025). CS 3080: Python programming,
#   Lectures 7 & 8: Memory management, file handling, dunder methods
#   [PowerPoint slides]. Department of Computer Science, University of Colorado Colorado Springs.