# LoginApp.py
# ==================================
# Hospital Bed Management – Login
# Tkinter GUI with FastAPI backend
# ==================================
# 
# Purpose of the code:
#   - Provides a graphical login interface (username & password)
#   - Send credentials to the FastAPI backend for verification
#   - Display success or error messages based on the backend response.
#
# Design notes:
#   - tkinter is python's standard GUI library (Python Software Foundation, 2025a)
#   - Widgets such as Label, Entry, and Button follow common usage patterns
#     described in Tkinter tutorials and references (Shipman, 2013; TkDocs, 2024; Real Python, 2024)
#   - The requests library is used to communicate with the HTTP API exposed by FastAPI
#     (Python Software Foundation, 2024b; Tiangolo, 2024)
#   
# -----Imports-------
# 'sys' is Python's built-in system module that provides access to the interpreter’s runtime environment
# Used here to modify sys.path for dynamic module imports (Python Software Foundation, 2025)
import sys
import os  # File path utility (Python Software Foundation, 2025b)
# Tkinter core library for GUI

# Add the bedbuddy root to the Python import path. This will let LoginApp.py
# import ui modules even when the program is launched from another directory.
# (Python Software Foundation, 2024; ZohourianShahzadi, 2025, Lec. 7-8)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
# ttk for themed widgets and messagebox for pop-ups
from tkinter import ttk, messagebox, PhotoImage
from fastapi import status  # symbolic HTTP status codes for clarity (Tiangolo, 2025)
import platform  # Detect Operating System (Python Software Foundation, 2025c)
import requests  # For HTTP requests to FastAPI backend (Reitz & Chisamore, 2024)
from ui.bedbuddy_ui import BedBuddy  # BedBuddy main application window

def asset_path(filename: str) -> str:
    '''
    Builds the full path to a file inside the assets folder.

    This avoids issues where Tkinter looks in the wrong directory.
    It works by,
    -finding where this file LoginApp.py is located
    -Moving up to the main project. folder
    -Adding the assets folder name
    -Joining that with the filename we want

    (Python Software Foundation, 2024; ZohourianShahzadi, 2025, Lec. 7-8))
    '''
    # Location of LoginApp.py (ui folder) bedbuddy/ui
    ui_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the bedbuddy folder bedbuddy/
    bedbuddy_dir = os.path.dirname(ui_dir)
    # Points to the assets folder bedbuddy/assets
    assets_dir = os.path.join(bedbuddy_dir, "assets")
    # Build the final path
    return os.path.join(assets_dir, filename)

# ------------------
# Login Window Class
# ------------------
# Define a Login class that inherits from Tkinter's root window (tk.Tk)
class Login(tk.Tk):
    '''GUI login window integrated with FastAPI authentication backend'''

    def __init__(self):
        ''' Initializes the login window layout and widget configuration.'''
        super().__init__()  # Initialize parent Tkroot window
        self.title("Bed Management – Login")  # Set window title
        self.geometry("400x350")  # Set window size
        self.resizable(False, False)  # Disable resizing

        # Handles icons Cross-platform window (Python Software Foundation, 2025a)
        try:
            if platform.system() == "Windows":
                # Windows prefers .ico format
                self.iconbitmap(asset_path("BBLogo.ico"))
            else:
                # macOS/Linux fallback (PNG)
                self.iconphoto(False, PhotoImage(file=asset_path("BBLogo.png")))
        except Exception as e:
            print("Icon not loaded:", e)

        # Create a frame with padding to hold the widgets (TkDocs, 2024)
        frame = ttk.Frame(self, padding=16)
        # Expand to fill the window
        frame.pack(fill="both", expand=True)

        # Load clickable logo button (TkDocs, 2024)
        try:
            self.logo_img = PhotoImage(file=asset_path("BBLogo.png"))  # load png logo
            self.logo_img = self.logo_img.subsample(8, 8)  # shrink by factor of 8
            logo_button = tk.Button(
                frame,
                image=self.logo_img,
                command=self.show_about,  # clickable logo opens info
                borderwidth=0,
                highlightthickness=0
            )
            logo_button.grid(row=0, column=0, columnspan=2, pady=10)
        except Exception as e:
            print("Logo not found", e)

        # Username label and entry field
        ttk.Label(frame, text="username").grid(row=1, column=0, sticky="w")
        self.e_user = ttk.Entry(frame, width=26)  # Input box for username
        self.e_user.grid(row=1, column=1, pady=4)

        # Password label and entry field (hidden with * for security)
        ttk.Label(frame, text="password").grid(row=2, column=0, sticky="w")
        self.e_pass = ttk.Entry(frame, show="*", width=26)
        self.e_pass.grid(row=2, column=1, pady=4)

        # Label for status/error messages (red text)
        self.status = ttk.Label(frame, text="", foreground="red")
        self.status.grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 2))

        # "Sign In" button triggers do_login()
        ttk.Button(frame, text="Sign In", command=self.do_login).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0)
        )

        # Allow pressing Enter/Return to login
        self.bind("<Return>", lambda e: self.do_login())

        # Configure grid so both columns expand evenly
        for i in range(2):
            frame.grid_columnconfigure(i, weight=1)

    # Show an About dialog when logo is clicked
    def show_about(self):
        messagebox.showinfo("About", "Hospital Bed Management System\n" \
                                     "CS 3300 Project\nDeveloped by BedBuddy")

    # Main login logic: FastAPI Integration
    def do_login(self):
        ''' Attempt to log in a user through the FastAPI backend

            Steps:
            1. Read the username and password typed into the login form
            2. Send the data to the backend endpoints '/auth/login' using http POST
               (Reitz & Chisamore, 2024; Tiangolo, 2024)
            3. If backend confimrs login (response 200), display a success message and close the window
            4. If backend rejects login, display 401 error message in red (Tiangolo, 2024)
            5. If backend cannot be reached, show a server error message

        '''
        username = self.e_user.get().strip()  # Get the entered username (remove spaces)
        password = self.e_pass.get()  # Get the entered password

        try:
            ''' Send a request to the FastAPI backend at the /auth/login address
                We are using the HTTP "POST" method which means:
                - We are sending data to the server (username & password)
                - The server will process the data and give us a respionse
                (REitz & Chisamore, 2024; Tiangolo, 2024)
            '''
            response = requests.post(
                "http://127.0.0.1:8000/auth/login", json={
                    "username": username,  # Take the username. from the Tkinter form
                    "password": password  # Take the password from the Tkinter form
                })

            # If the server responds with status code 200, it means login worked
            # (Tiangolo, 2025)
            if response.status_code == status.HTTP_200_OK:
                # Convert the server's JSON reply into a Python dictionary
                data = response.json()

                # Get the "access_token" from the reply
                # This token is a JSON web token (JWT) used to prove the user is logged in
                # (Davis, 2024)
                access_token = data.get("access_token")

                # Show a success message in a Tkinter popup
                messagebox.showinfo("Success", "Login successful.")
                # Close the login window
                self.destroy()

                # Launch the BedBuddy main interface (after successful login)
                try:
                    app = BedBuddy()  # Create an instance of main UI
                    app.run()  # Start BedBuddy interface

                except Exception as e:
                    messagebox.showerror("Error", f"Unable to launch BedBuddy UI")
                    raise  # testing error

            elif response.status_code == status.HTTP_401_UNAUTHORIZED:

                # GUI first looks for the detail field returned by FastAPI.
                # If it’s not there, it defaults to a generic message "Login
                # failed" so users still see feedback (Tiangolo, 2025)
                error_message = response.json().get("detail", "Login failed")
                self.status.config(text=error_message)

            else:
                # Handles other possible status codes, a catch all.
                messagebox.showerror(
                    "Error",
                    f"Unexpected response ({response.status_code}): {response.text}"
                )


        # Handles cases like server down, no internet connection(Reitz & Chisamore, 2024)
        except requests.exceptions.RequestException as error:
            messagebox.showerror(
                "Connection Error",
                f"Could not connect to the FastAPI backend:\n{error}"
            )

'''
This application was developed using open-source libraries and documentation .
All code patterns and examples were adapted from the cited sources.

References:
Davis, M. P. (2024). python-jose: JWT library for Python. GitHub. 
    https://github.com/mpdavis/python-jose
Jose project team. (2024). PyJWT documentation. PyJWT. 
    https://pyjwt.readthedocs.io/
National Institute of Standards and Technology. (2020). Digital 
    identity guidelines: Authentication and lifecycle management 
    (NIST Special Publication 800-63B). U.S. Department of Commerce. 
    https://doi.org/10.6028/NIST.SP.800-63b
Python Software Foundation. (2025, October 29). tkinter — Python 
    interface to Tcl/Tk. In Python 3.13 documentation. 
    https://docs.python.org/3/library/tkinter.html
Python Software Foundation. (2025, October 29). os — Miscellaneous 
    operating system interfaces. In Python 3.13 documentation. 
    https://docs.python.org/3/library/os.html
Python Software Foundation. (2024). Modules and packages — Import system. 
    In The Python 3.13 documentation. https://docs.python.org/3/tutorial/modules.html
Python Software Foundation. (2025, October 29). platform — Access 
    to underlying platform’s identifying data. In Python 3.13 documentation. 
    https://docs.python.org/3/library/platform.html
Python Software Foundation. (2025). sys — System-specific parameters and functions. 
    In Python 3.13 documentation. https://docs.python.org/3/library/sys.html
Reitz, K., & Chisamore, E. (2024). Requests: HTTP for humans. 
    Python Requests. https://requests.readthedocs.io/
Shipman, J. W. (2013). Tkinter 8.5 reference: A GUI for Python. 
    New Mexico Tech Computer Center. https://tkdocs.com/shipman/
TkDocs. (2024). TkDocs tutorial: Basic widgets. https://tkdocs.com/tutorial/widgets.html    
Tiangolo, S. (2025). FastAPI documentation. FastAPI. 
    https://fastapi.tiangolo.com/
Real Python. (2024). Python GUI programming: Your Tkinter tutorial. 
    Real Python. https://realpython.com/python-gui-tkinter/

ZohourianShahzadi, Z. (2025). CS 3080: Python programming, 
    Lectures 7 & 8: Memory management, file handling, dunder methods 
    [PowerPoint slides]. Department of Computer Science, 
    University of Colorado Colorado Springs.
'''