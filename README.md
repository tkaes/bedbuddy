# BedBuddy: ER Bed Management System
## Authors: BedBuddy Development Team
(Fall 2025, UCCS CS 3300)
## Last Updated: 26 November 2025

BedBuddy is a prototype desktop application built for emergency room settings to help track patients and bed availability.
It combines a Tkinter graphical interface with a FastAPI backend that connects to a MongoDB Atlas cloud database.
The application demonstrates secure login authentication, patient management, and bed assignment features using modular,
testable components that can be expanded into a full system.

# System Requirements:
Before running, ensure you have the following:
1. Python 3.11 - 3.12 installed
2. MongoDB Atlas cluster & URI string
3. A working internet connection
4. Git

### Python Notes:
Bedbuddy has been tested on Python 3.11 and 3.12, inside a virtual environment to avoid dependency conflicts. During testing, there were dependency conflicts with Python version 3.13 and above. Please install Python 3.11.x or Python 3.12.x for full compatibility. 

### Packages Used:
* FastAPI - backend framework (Tiangolo, 2025)
* pymongo - MongoDB driver (MongoDB Inc., 2025)
* Motor - async MongoDB driver (MongoDB Inc., 2025)
* passlib[argon2] - secure password hashing (The Passlib Project, 2024)
* Python-jose - JWT signing and verification (Davis, 2024)
* Python-dotenv - for loading environment variables from local machine
* requests - sends HTTP POST requests from Tkinter GUI app to communicate with FastAPI server (Reitz & Chisamore, 2024)
* tkinter, ttk - Python's built-in GUI toolkit (Python Software Foundation, 2025)

# Setup Guide (macOS & Windows)
This guide is intended to prepare the computer to run BedBuddy locally.
We use a .env file instead of hard-coding credentials to follow real-world security practices.
This approach helps prevent accidental exposure and follows common software security guidelines (OWASP Foundation, 2023). 

1. Clone the repository

    `git clone https://github.com/<your-team-repo>/bedbuddy.git`
    <br>
    `cd bedbuddy`

2. Create and activate a virtual environment (Recommended)
    
    This ensures everyone uses the same Python version and avoids dependency issues.
    During testing, there were version conflicts with FastAPI, Motor, and Argon2 using Python version 3.13 and above.
    The steps below will create a virtual environment with Python 3.12 version.
    
    ## macOS
    https://www.python.org/downloads/macos/ | macOS Python download versions
    
    The first command tells Python 3.12 to create a new isolated environment named "bedbuddy".
    You can modify the name of your virtual environment or the python version.
    <br>
    `python3.12 -m venv bedbuddy`
    
    The second command activates that environment so you can install dependencies without affecting your system.
    <br>
    `source bedbuddy/bin/activate`

    ## Windows (PowerShell)
    The first command tells Python 3.12 to create a new isolated environment named "bedbuddy".
    You can modify the name of your virtual environment or the python version.
    <br>
    `py -3.12 -m venv bedbuddy`
    
    The second command activates that environment so you can install dependencies without affecting your system.
    <br>
    `.\bedbuddy\Scripts\activate`

3. Install project dependencies
    
    Ensure you are inside the backend/ directory.
    <br>
    `cd backend`
    These dependencies support the backend, password hashing, JWT token creation, environment variable, and the communication between the UI and the backend. 
    <br>
    `pip install -r requirements.txt`
    
    <img width="567" height="411" alt="Screenshot 2025-11-19 at 12 34 41" src="https://github.com/user-attachments/assets/c0c43e54-6bb4-403a-8d8e-12ab44296f7f" />
    
    The file includes:
   * fastapi
   * uvicorn
   * motor
   * passlib[argon2]
   * python-jose[cryptography]
   * python-dotenv
   * requests
   * pymongo
   * argon2-cffi

5. Create your personal .env file
    
    Create a file titled .env in the backend folder.
    Git should not recognize changes to it.
   <br>
    `touch .env`
   
   Paste the following information in the file as follows:
   ```
   MONGO_URI=<your MongoDB Atlas connection string>
   DB_NAME=bedbuddy
   JWT_SECRET=<your generated key>
   JWT_ALGORITHM=HS256
   ```

6. OPTIONAL: Generate your own JWT secret key
    A JWT secret key is a secure, long, random, and private string that will be used to sign the JWT to the backend (Python Software Foundation, 2025).
    There is an easy approach using the terminal to generate one.
    <br>
    `python -c "import os; print(os.urandom(24).hex())"`

   The command uses Python’s built-in os.urandom function, to generate 24 random bytes and converts them into a hexadecimal string.
   This approach is commonly used to generate secret keys and other security sensitive data (Python Software Foundation, 2025).

   Copy the generated key:
   
        Example: 4f7e8b09f7a3d85e23fa0a74b3409b987dc307c3f3b7a9e8
   
    Paste it into your .env file.
    Keep your key safe and private.

# Running the Backend:

1. Open a terminal and go to the backend folder.

    `cd backend`

2. Start the FastAPI server.

    `uvicorn auth_api:app --reload`

    You should see:
    `Uvicorn running on http://127.0.0.1:8000`

    <img width="564" height="172" alt="Screenshot 2025-11-08 at 19 35 39" src="https://github.com/user-attachments/assets/9e8bae7c-f7d2-4bed-8ba2-76b8940c6238" />

3. Open Swagger UI
    Go to http://127.0.0.1:8000/docs
    
    FastAPI automatically generates a test interface where you can try both endpoints.
    
    <img width="185" height="165" alt="image" src="https://github.com/user-attachments/assets/ac81b3b1-393c-4290-9d85-af21a831b4de" />
    
    From here, you can test:
    
    /auth/register         Register a new user      Returns 201 Created and "msg: User registered successfully"
    
    <img width="186" height="105" alt="image" src="https://github.com/user-attachments/assets/4760b786-599a-45f0-acf3-6b734d69b190" />
    
    /auth/login            Log in existing user     Returns 200 ok and a JWT token
    
    <img width="203" height="109" alt="image" src="https://github.com/user-attachments/assets/351a1970-ddef-419b-8add-2a1022ebe8e2" />
    
    /auth/login            Invalid credentials      Returns 401 Unauthorized with "Failed Login"
    
    <img width="170" height="161" alt="image" src="https://github.com/user-attachments/assets/ce61002d-a659-467c-a37e-8afcaf4d7ed7" />

# Running the Tkinter Login App

1. Open a second terminal while keeping Uvicorn running:
    <br>
    **python LoginApp.py**
    <br>
    <img width="265" height="245" alt="image" src="https://github.com/user-attachments/assets/29edeb94-4179-4f84-9b2e-1b785bff3538" />

3. Enter the same credentials used in your registration test.
    <br>
    **"Login Successful"**
    <br>
    <img width="151" height="143" alt="image" src="https://github.com/user-attachments/assets/e5f81c45-059e-4a04-bd8f-5b1b0c1febae" />
    <br>
    **"Invalid username or password"**
    <br>
    <img width="400" height="380" alt="Screenshot 2025-11-06 at 23 15 28" src="https://github.com/user-attachments/assets/78f962ff-6a2d-4059-a4a8-abf383d4ca74" />

5. Verify Database Update
    <br>
    **MongoDB Database user registration verification with password hashing**
    <br>
    <img width="255" height="129" alt="image" src="https://github.com/user-attachments/assets/c24e4a65-4c1f-4393-9510-9bf0a411263f" />
    <br>
    **MongoDB Database user registration verification (closer look)**
    <br>
    <img width="468" height="102" alt="image" src="https://github.com/user-attachments/assets/175db301-de78-4491-b77c-faaecd7bca9b" />

# Summary:
  * Passwords are never stored in plain text
  * Each password is hashed using Argon2
  * The backend issues JWT tokens signed with the secret key defined in .env
  * Tokens are time-limited and must be reissued upon expiration
  * In a real healthcare setting, authentication and data privacy would comply with HIPAA / NIST SP 800-63B.
  * The BedBuddy project incorporates this principle for demonstration and best practice learning. 

# Backend Code Overview:

**auth_api.py**
<br>
Implements two endpoints:
  * POST /auth/register - creates a user in MongoDB after hashing the password
  * POST /auth/login - verifies credentials and returns a JWT token

**secrets.py**
<br>
This code implements:
  * hash_password() and verify_password() using Passlib Argon2
  * create_access_token() using python-jose
  * Loads keys/secrets from .env using python-dotenv

# References:

Davis, M. P. (2024). python-jose: JWT library for Python. GitHub. https://github.com/mpdavis/python-jose

MongoDB Inc. (2025). Motor: Asynchronous Python driver for MongoDB. https://motor.readthedocs.io

TkDocs. (2024). Tkinter Tutorial. https://tkdocs.com

The Passlib Project. (2024). Passlib: Password hashing framework for Python. https://passlib.readthedocs.io

Tiangolo, S. (2025). FastAPI documentation. https://fastapi.tiangolo.com

OWASP Foundation. (2023). OWASP cheat sheet series: Secrets management. https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

Python Software Foundation. (2025). tkinter — Python interface to Tcl/Tk. https://docs.python.org/3/library/tkinter.html

Python Software Foundation. (2025). os — Miscellaneous operating system interfaces. https://docs.python.org/3/library/os.html

Python Software Foundation. (2025). platform — Access to underlying platform data. https://docs.python.org/3/library/platform.html

Real Python. (2024). Python Tkinter Tutorial. https://realpython.com/python-gui-tkinter/

Reitz, K., & Chisamore, E. (2024). Requests: HTTP for Humans. https://requests.readthedocs.io

National Institute of Standards and Technology. (2020). Digital Identity Guidelines: Authentication and Lifecycle Management (NIST SP 800-63B). U.S. Department of Commerce. https://doi.org/10.6028/NIST.SP.800-63b

Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education.

