# Entry point for the BedBuddy application

# This module initializes the system by:
#   1. Retrieves patient records from the MongoDB Atlas database
#   2. Displays basic patient info
#   3. Launches the BedBuddy graphical interface
#--------------
# Design Notes:
#--------------
# - This script acts as the "controller" connecting the database (model) and UI (view),
#   which follows the MVC (Model–View–Controller) design principle.
# - Using separate modules for database operations and the UI improves maintainability
#   and supports Agile/iterative development practices.
# -----------
# References:
# -----------
# - Python Software Foundation. (2024). The Python Tutorial: Modules and Packages*. 
#  https://docs.python.org/3/tutorial/modules.html
# - MongoDB, Inc. (2025). PyMongo – Python driver for MongoDB. 
# https://pymongo.readthedocs.io/
# - Python Software Foundation. (2024). tkinter — Python interface to Tcl/Tk. 
#  https://docs.python.org/3/library/tkinter.html
# - Reenskaug, T. (1979). Model-View-Controller (MVC) architecture pattern.
#   Xerox PARC technical note.
# - Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education.
# ====================================================================================

from ui.LoginApp import Login

# Entry point: run Login GUI
if __name__ == "__main__":
    Login().mainloop()
