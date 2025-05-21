"""
main.py

This module initializes and starts the Password Manager GUI application using Tkinter.

Classes:
    PasswordManagerGUI: The main GUI class for the password manager.

Functions:
    main(): Creates the main application window, initializes the PasswordManagerGUI, and starts the Tkinter event loop.

Usage:
    Run this module directly to start the Password Manager GUI application.

Example:
    python main.py

Dependencies:
    tkinter: Standard Python interface to the Tk GUI toolkit.
    password_manager_gui: Custom module containing the PasswordManagerGUI class.

"""

import tkinter as tk
from password_manager_gui import PasswordManagerGUI

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Initialize the PasswordManagerGUI with the main window
    app = PasswordManagerGUI(root)

    # Start the Tkinter event loop
    root.mainloop()
