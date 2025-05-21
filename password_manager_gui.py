"""
password_manager_gui.py

This module provides the PasswordManagerGUI class to create the main interface for the password manager application using Tkinter.
It interacts with the PasswordManager class for backend functionality and includes features such as password strength checking,
password generation, and secure storage.

Classes:
    PasswordManagerGUI: The main GUI class for the password manager application.

Functions:
    __init__(self, root): Initializes the PasswordManagerGUI with the main window.
    configure_styles(self): Configures custom styles for the GUI.
    create_login_frame(self): Creates the login frame for the application.
    show_unlock_dialog(self): Shows the unlock dialog for the vault.
    try_unlock_vault(self, master_password, dialog): Attempts to unlock the vault with the provided master password.
    show_create_vault_dialog(self): Shows the dialog to create a new vault.
    create_new_vault_with_password(self, password, confirm_password, dialog): Creates a new vault with the provided password.
    create_new_vault(self): Creates a new vault.
    create_main_interface(self): Creates the main interface of the application.
    create_sidebar(self): Creates the sidebar for the application.
    create_content_area(self): Creates the content area for the application.
    create_top_bar(self): Creates the top bar for the application.
    create_split_view(self): Creates the split view for the application.
    create_details_pane(self): Creates the details pane for viewing/editing password details.
    load_password_list(self, category="All Passwords"): Loads passwords into the treeview based on the selected category.
    sort_treeview(self, column): Sorts the treeview by the specified column.
    search_passwords(self, *args): Filters the password list based on the search query.
    handle_category_selection(self, event): Handles the selection of a category in the sidebar.
    add_new_password(self): Shows the dialog to add a new password.
    update_password_strength(self, password, strength_meter, strength_label, feedback_label): Updates the password strength meter.
    generate_and_set_password(self, password_var, strength_meter, strength_label, feedback_label): Generates a password and updates the strength meter.
    save_new_password(self, service, username, password, url, notes, dialog): Saves a new password to the vault.
    edit_password(self, service, username): Shows the dialog to edit an existing password.
    update_password(self, old_service, old_username, new_service, new_username, new_password, new_url, new_notes, dialog): Updates an existing password.
    delete_password(self, service, username): Deletes a password from the vault.
    copy_to_clipboard(self, text): Copies text to the clipboard.
    toggle_password_visibility(self): Toggles password visibility between hidden and shown.
    show_password_details(self, event): Shows details of the selected password.
    generate_password(self): Shows the dialog to generate a password.
    generate_and_display_password(self, length, include_uppercase, include_lowercase, include_digits, include_special, password_var): Generates a password based on settings and displays it.
    open_settings(self): Opens the settings dialog.
    change_master_password(self, current_password, new_password, confirm_password, dialog): Changes the master password.
    lock_vault(self): Locks the vault and returns to the login screen.

Dependencies:
    os: Standard library for interacting with the operating system.
    pyperclip: Module for cross-platform clipboard operations.
    tkinter: Standard Python interface to the Tk GUI toolkit.
    password_strength_checker: Custom module for checking password strength.
    password_manager: Custom module containing the PasswordManager class.
"""

import os
import pyperclip
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from password_strength_checker import check_password_strength
from password_manager import PasswordManager

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.password_manager = PasswordManager()

        # Configure the window to open in full screen
        self.root.title("Secure Password Manager")
        self.root.state('zoomed')  # Full screen on Windows

        # Set the theme to a clean, light theme (Apple-inspired)
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure styles
        self.configure_styles()

        # Create login frame first
        self.create_login_frame()

    def configure_styles(self):
        """Configure custom styles for the GUI"""
        # Main background color
        self.root.configure(background="#1E1E1E")

        # Button style
        self.style.configure(
            'TButton',
            background='#3D3D3D',
            foreground='white',
            font=('Helvetica', 11),
            borderwidth=0,
            focuscolor='#4D4D4D',
            padding=6
        )
        self.style.map(
            'TButton',
            background=[('active', '#4D4D4D')],
            foreground=[('active', 'white')]
        )

        # Primary action button style
        self.style.configure(
            'Primary.TButton',
            background='#4D4D4D',
            foreground='white',
            font=('Helvetica', 11, 'bold'),
            padding=6
        )
        self.style.map(
            'Primary.TButton',
            background=[('active', '#5D5D5D')]
        )

        # Label style
        self.style.configure(
            'TLabel',
            background='#1E1E1E',
            foreground='#CCCCCC',
            font=('Helvetica', 11),
            padding=4
        )

        # Entry style
        self.style.configure(
            'TEntry',
            fieldbackground='#2D2D2D',
            foreground='white',
            insertcolor='white',
            padding=8,
            font=('Helvetica', 11)
        )

        # Treeview style (for list)
        self.style.configure(
            'Treeview',
            background='#2D2D2D',
            foreground='#CCCCCC',
            fieldbackground='#2D2D2D',
            font=('Helvetica', 11)
        )
        self.style.map(
            'Treeview',
            background=[('selected', '#4D4D4D')],
            foreground=[('selected', 'white')]
        )
        self.style.configure(
            'Treeview.Heading',
            background='#3D3D3D',
            foreground='white',
            font=('Helvetica', 12, 'bold')
        )

        # Tab style
        self.style.configure(
            'TNotebook',
            background='#1E1E1E',
            tabmargins=[2, 5, 2, 0]
        )
        self.style.configure(
            'TNotebook.Tab',
            background='#2D2D2D',
            foreground='#CCCCCC',
            padding=[10, 5],
            font=('Helvetica', 11)
        )
        self.style.map(
            'TNotebook.Tab',
            background=[('selected', '#3D3D3D')],
            foreground=[('selected', 'white')],
            expand=[('selected', [1, 1, 1, 0])]
        )

        # Frame style
        self.style.configure(
            'TFrame',
            background='#1E1E1E'
        )

        # Search container style
        self.style.configure(
            'SearchContainer.TFrame',
            background='#2D2D2D',
            borderwidth=1,
            relief='solid'
        )

        # Dark listbox style
        self.listbox_bg = '#2D2D2D'
        self.listbox_fg = '#CCCCCC'
        self.listbox_select_bg = '#4D4D4D'
        self.listbox_select_fg = 'white'

        # Custom separator style
        self.style.configure(
            'TSeparator',
            background='#3D3D3D'
        )

        # Custom style for LabelFrame
        self.style.configure(
            'TLabelframe',
            background='#1E1E1E',
            foreground='#CCCCCC',
            padding=10
        )
        self.style.configure(
            'TLabelframe.Label',
            background='#1E1E1E',
            foreground='#CCCCCC',
            font=('Helvetica', 11, 'bold')
        )

        # Add colored progress bar styles for password strength
        self.style.configure('Green.Horizontal.TProgressbar',
                             background='green',
                             troughcolor='#2D2D2D')
        self.style.configure('Yellow.Horizontal.TProgressbar',
                             background='#FFCC00',
                             troughcolor='#2D2D2D')
        self.style.configure('Orange.Horizontal.TProgressbar',
                             background='orange',
                             troughcolor='#2D2D2D')
        self.style.configure('Red.Horizontal.TProgressbar',
                             background='red',
                             troughcolor='#2D2D2D')

    def create_login_frame(self):
        """Create the login interface with options to create or unlock vault"""
        self.login_frame = ttk.Frame(self.root, padding="40 40 40 40")
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Center the login form
        self.login_form = ttk.Frame(self.login_frame)
        self.login_form.pack(expand=True, anchor=tk.CENTER)

        # Logo and title
        title_label = ttk.Label(self.login_form, text="Secure Password Manager",
                                font=('Helvetica', 22, 'bold'), foreground='white')
        title_label.pack(pady=(0, 30))

        # Welcome message
        welcome_label = ttk.Label(self.login_form,
                                  text="Welcome to Secure Password Manager",
                                  font=('Helvetica', 14), foreground='#CCCCCC')
        welcome_label.pack(pady=(0, 20))


        # Option buttons
        button_frame = ttk.Frame(self.login_form)
        button_frame.pack(fill=tk.X, pady=20)

        create_button = ttk.Button(button_frame, text="Create New Vault",
                                   command=self.show_create_vault_dialog, width=20)
        create_button.pack(side=tk.TOP, pady=10)

        unlock_button = ttk.Button(button_frame, text="Unlock Existing Vault",
                                   command=self.show_unlock_dialog, style='TButton', width=20)
        unlock_button.pack(side=tk.TOP, pady=10)

        # Load and display the logo image
        self.logo_image = tk.PhotoImage(file="img.png")
        logo_label = ttk.Label(self.login_frame, image=self.logo_image)
        logo_label.pack(side=tk.TOP ,pady=(0, 20))  # Increase the bottom padding to 20 # Adjust the bottom padding to 10

    def show_unlock_dialog(self):
        """Show dialog to unlock an existing vault"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Unlock Vault")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()  # Make dialog modal

        # Apply the same style
        dialog.configure(background="#F5F5F7")

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Master password entry
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=10)

        password_label = ttk.Label(password_frame, text="Master Password", font=('Helvetica', 11))
        password_label.pack(anchor=tk.W, pady=(0, 5))

        password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=password_var,
                                   show="•", width=30, font=('Helvetica', 12))
        password_entry.pack(fill=tk.X, pady=5)
        password_entry.focus()

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=20)

        cancel_button = ttk.Button(button_frame, text="Cancel",
                                   command=dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        unlock_button = ttk.Button(button_frame, text="Unlock",
                                   command=lambda: self.try_unlock_vault(password_var.get(), dialog),
                                   style='TButton')
        unlock_button.pack(side=tk.RIGHT, padx=5)

        # Bind Enter key to unlock
        password_entry.bind('<Return>', lambda event: self.try_unlock_vault(password_var.get(), dialog))

    def try_unlock_vault(self, master_password, dialog):
        """Try to unlock the vault with the provided master password"""
        if not master_password:
            messagebox.showerror("Error", "Please enter your master password")
            return

        # Try to initialize the password manager
        self.password_manager.initialize(master_password)

        if self.password_manager.initialized:
            dialog.destroy()
            self.login_frame.destroy()
            self.create_main_interface()
        else:
            messagebox.showerror("Authentication Failed", "Incorrect master password")

    def show_create_vault_dialog(self):
        """Show dialog to create a new vault"""
        # Check if a vault already exists
        if os.path.exists(self.password_manager.vault_file):
            confirm = messagebox.askyesno("Warning",
                                          "A vault already exists. Creating a new vault will overwrite it. Continue?")
            if not confirm:
                return

        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Vault")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()  # Make dialog modal

        # Apply the same style
        dialog.configure(background="#F5F5F7")

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Master password entry
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=10)

        password_label = ttk.Label(password_frame, text="New Master Password", font=('Helvetica', 11))
        password_label.pack(anchor=tk.W, pady=(0, 5))

        password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=password_var,
                                   show="•", width=30, font=('Helvetica', 12))
        password_entry.pack(fill=tk.X, pady=5)
        password_entry.focus()

        # Confirm password entry
        confirm_frame = ttk.Frame(form_frame)
        confirm_frame.pack(fill=tk.X, pady=10)

        confirm_label = ttk.Label(confirm_frame, text="Confirm Master Password", font=('Helvetica', 11))
        confirm_label.pack(anchor=tk.W, pady=(0, 5))

        confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(confirm_frame, textvariable=confirm_var,
                                  show="•", width=30, font=('Helvetica', 12))
        confirm_entry.pack(fill=tk.X, pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=20)

        cancel_button = ttk.Button(button_frame, text="Cancel",
                                   command=dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        create_button = ttk.Button(button_frame, text="Create Vault",
                                   command=lambda: self.create_new_vault_with_password(
                                       password_var.get(), confirm_var.get(), dialog),
                                   style='TButton')
        create_button.pack(side=tk.RIGHT, padx=5)

        # Bind Enter key to create
        confirm_entry.bind('<Return>', lambda event: self.create_new_vault_with_password(
            password_var.get(), confirm_var.get(), dialog))

    def create_new_vault_with_password(self, password, confirm_password, dialog):
        """Create a new vault with the provided password"""
        if not password:
            messagebox.showerror("Error", "Please enter a master password")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Create new vault
        self.password_manager.initialize(password)

        if self.password_manager.initialized:
            dialog.destroy()
            self.login_frame.destroy()
            self.create_main_interface()
            messagebox.showinfo("Success", "New vault created successfully")
        else:
            messagebox.showerror("Error", "Failed to create new vault")

    def create_new_vault(self):
        """Show dialog to create a new vault"""
        self.show_create_vault_dialog()

    def create_main_interface(self):
        """Create the main password manager interface"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the sidebar and content area
        self.create_sidebar()
        self.create_content_area()

        # Initially load all passwords
        self.load_password_list()

    def create_sidebar(self):
        """Create the sidebar with categories"""
        self.sidebar = ttk.Frame(self.main_frame, padding="10 20 10 20", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)  # Prevent the frame from shrinking

        # Title
        title_frame = ttk.Frame(self.sidebar)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        sidebar_title = ttk.Label(title_frame, text="Categories",
                                  font=('Helvetica', 14, 'bold'))
        sidebar_title.pack(side=tk.LEFT)

        # Categories list with custom styling
        self.category_listbox = tk.Listbox(self.sidebar,
                                           font=('Helvetica', 11),
                                           bg='grey',
                                           fg='white',
                                           selectbackground='light grey',
                                           selectforeground='#333333',
                                           borderwidth=0,
                                           highlightthickness=0,
                                           activestyle='none')
        self.category_listbox.pack(fill=tk.BOTH, expand=True)

        # Add default categories
        self.category_listbox.insert(tk.END, "All Passwords")
        self.category_listbox.insert(tk.END, "Recently Used")
        self.category_listbox.insert(tk.END, "Recently Added")

        # Add a separator
        self.category_listbox.insert(tk.END, "─" * 22)

        # Bind selection event
        self.category_listbox.bind('<<ListboxSelect>>', self.handle_category_selection)

        # Select "All Passwords" by default
        self.category_listbox.selection_set(0)

        # Buttons at the bottom
        button_frame = ttk.Frame(self.sidebar)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        settings_button = ttk.Button(button_frame, text="Settings",
                                     command=self.open_settings)
        settings_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        lock_button = ttk.Button(button_frame, text="Lock Vault",
                                 command=self.lock_vault)
        lock_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

    def create_content_area(self):
        """Create the main content area with password list and details"""
        self.content_frame = ttk.Frame(self.main_frame, padding="20")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Top search and buttons bar
        self.create_top_bar()

        # Create split view (passwords list and details pane)
        self.create_split_view()

    def create_top_bar(self):
        """Create the top bar with search and buttons"""
        self.top_bar = ttk.Frame(self.content_frame, padding="0 0 0 10")
        self.top_bar.pack(fill=tk.X, pady=(0, 15))

        # Search frame
        search_frame = ttk.Frame(self.top_bar)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Search box with icon (simulated with label)
        search_container = ttk.Frame(search_frame, style='SearchContainer.TFrame')
        search_container.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Style for search container
        self.style.configure('SearchContainer.TFrame', background='grey', borderwidth=1, relief='solid')

        search_icon = ttk.Label(search_container, text="🔍", background='grey', font=('Helvetica', 11))
        search_icon.pack(side=tk.LEFT, padx=(8, 0))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.search_passwords)

        search_entry = ttk.Entry(search_container, textvariable=self.search_var,
                                 font=('Helvetica', 11), style='NoBorder.TEntry')
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        # Style for borderless entry
        self.style.configure('NoBorder.TEntry', borderwidth=0, padding=2)

        # Buttons frame
        button_frame = ttk.Frame(self.top_bar)
        button_frame.pack(side=tk.RIGHT)

        add_button = ttk.Button(button_frame, text="+ Add", command=self.add_new_password)
        add_button.pack(side=tk.LEFT, padx=5)

        generate_button = ttk.Button(button_frame, text="Generate", command=self.generate_password)
        generate_button.pack(side=tk.LEFT, padx=5)

    def create_split_view(self):
        """Create split view with passwords list and details pane"""
        # Container frame
        self.split_frame = ttk.Frame(self.content_frame)
        self.split_frame.pack(fill=tk.BOTH, expand=True)

        # Passwords list (left side)
        self.list_frame = ttk.Frame(self.split_frame, padding="0 0 10 0")
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create treeview with scrollbar
        columns = ("service", "username", "lastModified")
        self.password_tree = ttk.Treeview(self.list_frame, columns=columns, show="headings",
                                          selectmode="browse")

        # Configure columns
        self.password_tree.heading("service", text="Service", anchor=tk.W)
        self.password_tree.heading("username", text="Username", anchor=tk.W)
        self.password_tree.heading("lastModified", text="Modified", anchor=tk.W)

        self.password_tree.column("service", width=150, stretch=True, anchor=tk.W)
        self.password_tree.column("username", width=150, stretch=True, anchor=tk.W)
        self.password_tree.column("lastModified", width=100, stretch=False, anchor=tk.W)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.password_tree.yview)
        self.password_tree.configure(yscrollcommand=scrollbar.set)

        # Pack list and scrollbar
        self.password_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selection event
        self.password_tree.bind("<<TreeviewSelect>>", self.show_password_details)

        # Details pane (right side)
        self.details_frame = ttk.Frame(self.split_frame, padding="10 0 0 0", width=300)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.details_frame.pack_propagate(False)  # Prevent shrinking

        # Create empty details pane
        self.create_details_pane()

    def create_details_pane(self):
        """Create the details pane for viewing/editing password details"""
        # Clear previous content
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Selected item info
        selected = self.password_tree.selection()

        if not selected:
            # No item selected - show empty state
            empty_label = ttk.Label(self.details_frame, text="Select an item to view details",
                                    font=('Helvetica', 12), foreground='#777777')
            empty_label.pack(expand=True)
            return

        # Get selected item data
        item_id = selected[0]
        item_values = self.password_tree.item(item_id, "values")
        service = item_values[0]
        username = item_values[1]

        # Get full password data
        password_data = self.password_manager.get_password(service, username)
        if not password_data:
            return

        # Title section
        title_frame = ttk.Frame(self.details_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = ttk.Label(title_frame, text=service,
                                font=('Helvetica', 16, 'bold'))
        title_label.pack(side=tk.LEFT)

        # Action buttons
        action_frame = ttk.Frame(title_frame)
        action_frame.pack(side=tk.RIGHT)

        edit_button = ttk.Button(action_frame, text="Edit",
                                 command=lambda: self.edit_password(service, username))
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(action_frame, text="Delete",
                                   command=lambda: self.delete_password(service, username))
        delete_button.pack(side=tk.LEFT)

        # Details section
        details_container = ttk.Frame(self.details_frame)
        details_container.pack(fill=tk.BOTH, expand=True, pady=10)

        # Username field
        username_frame = ttk.Frame(details_container)
        username_frame.pack(fill=tk.X, pady=8)

        username_label = ttk.Label(username_frame, text="Username:", width=12, font=('Helvetica', 11, 'bold'))
        username_label.pack(side=tk.LEFT)

        username_value = ttk.Label(username_frame, text=username)
        username_value.pack(side=tk.LEFT)

        copy_username_btn = ttk.Button(username_frame, text="Copy", width=8,
                                       command=lambda: self.copy_to_clipboard(username))
        copy_username_btn.pack(side=tk.RIGHT)

        # Password field
        password_frame = ttk.Frame(details_container)
        password_frame.pack(fill=tk.X, pady=8)

        password_label = ttk.Label(password_frame, text="Password:", width=12, font=('Helvetica', 11, 'bold'))
        password_label.pack(side=tk.LEFT)

        password_hidden = "•" * len(password_data["password"])
        self.password_var = tk.StringVar(value=password_hidden)
        self.real_password = password_data["password"]
        password_value = ttk.Label(password_frame, textvariable=self.password_var)
        password_value.pack(side=tk.LEFT)

        copy_password_btn = ttk.Button(password_frame, text="Copy", width=8,
                                       command=lambda: self.copy_to_clipboard(self.real_password))
        copy_password_btn.pack(side=tk.RIGHT, padx=5)

        show_password_btn = ttk.Button(password_frame, text="Show", width=8,
                                       command=self.toggle_password_visibility)
        show_password_btn.pack(side=tk.RIGHT)

        # URL field (if present)
        if password_data["url"]:
            url_frame = ttk.Frame(details_container)
            url_frame.pack(fill=tk.X, pady=8)

            url_label = ttk.Label(url_frame, text="URL:", width=12, font=('Helvetica', 11, 'bold'))
            url_label.pack(side=tk.LEFT)

            url_value = ttk.Label(url_frame, text=password_data["url"])
            url_value.pack(side=tk.LEFT)

        # Notes field (if present)
        if password_data["notes"]:
            notes_frame = ttk.Frame(details_container)
            notes_frame.pack(fill=tk.X, pady=8)

            notes_label = ttk.Label(notes_frame, text="Notes:", width=12,
                                    font=('Helvetica', 11, 'bold'), anchor=tk.NW)
            notes_label.pack(side=tk.LEFT, anchor=tk.N)

            notes_value = tk.Text(notes_frame, height=5, width=30, font=('Helvetica', 11),
                                  wrap=tk.WORD, bd=1, relief=tk.SOLID)
            notes_value.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            notes_value.insert(tk.END, password_data["notes"])
            notes_value.config(state=tk.DISABLED)  # Make read-only

        # Last modified
        modified_frame = ttk.Frame(details_container)
        modified_frame.pack(fill=tk.X, pady=(15, 8))

        modified_label = ttk.Label(modified_frame, text=f"Last modified: {password_data['date_modified']}",
                                   font=('Helvetica', 9), foreground='#777777')
        modified_label.pack(side=tk.LEFT)

    def load_password_list(self, category="All Passwords"):
        """Load passwords into the treeview based on selected category"""
        # Clear current items
        for item in self.password_tree.get_children():
            self.password_tree.delete(item)

        # Get all services
        services = self.password_manager.get_all_services()

        # Add each password to the list
        for service in services:
            usernames = self.password_manager.get_usernames(service)
            for username in usernames:
                password_data = self.password_manager.get_password(service, username)
                item_values = (service, username, password_data["date_modified"])
                self.password_tree.insert("", tk.END, values=item_values)

        # Sort by service name
        self.sort_treeview("service")

    def sort_treeview(self, column):
        """Sort the treeview by the specified column"""
        items = [(self.password_tree.set(k, column), k) for k in self.password_tree.get_children('')]
        items.sort()

        # Rearrange items in the sorted positions
        for index, (val, k) in enumerate(items):
            self.password_tree.move(k, '', index)

    def search_passwords(self, *args):
        """Filter the password list based on search query"""
        query = self.search_var.get().lower()

        # Clear current items
        for item in self.password_tree.get_children():
            self.password_tree.delete(item)

        if not query:
            # If search is empty, show all passwords
            self.load_password_list()
            return

        # Get all services
        services = self.password_manager.get_all_services()

        # Filter and add matching passwords to the list
        for service in services:
            if query in service.lower():
                # Add all usernames for this service
                usernames = self.password_manager.get_usernames(service)
                for username in usernames:
                    password_data = self.password_manager.get_password(service, username)
                    item_values = (service, username, password_data["date_modified"])
                    self.password_tree.insert("", tk.END, values=item_values)
            else:
                # Check each username
                usernames = self.password_manager.get_usernames(service)
                for username in usernames:
                    if query in username.lower():
                        password_data = self.password_manager.get_password(service, username)
                        item_values = (service, username, password_data["date_modified"])
                        self.password_tree.insert("", tk.END, values=item_values)

    def handle_category_selection(self, event):
        """Handle selection of a category in the sidebar"""
        selection = self.category_listbox.curselection()
        if not selection:
            return

        category = self.category_listbox.get(selection[0])

        # Skip if it's the separator
        if "─" in category:
            return

        # Load passwords based on selected category
        self.load_password_list(category)

    def add_new_password(self):
        """Show dialog to add a new password"""
        # Create a new top-level window
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Password")
        dialog.geometry("500x450")  # Increased height for strength meter
        dialog.transient(self.root)
        dialog.grab_set()  # Make dialog modal

        # Apply the same style
        dialog.configure(background="#F5F5F7")

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Service
        service_label = ttk.Label(form_frame, text="Service:", font=('Helvetica', 11))
        service_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        service_var = tk.StringVar()
        service_entry = ttk.Entry(form_frame, textvariable=service_var, width=40)
        service_entry.grid(row=0, column=1, sticky=tk.W + tk.E, pady=(0, 10))
        service_entry.focus()

        # Username
        username_label = ttk.Label(form_frame, text="Username:", font=('Helvetica', 11))
        username_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

        username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=username_var, width=40)
        username_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # Password
        password_label = ttk.Label(form_frame, text="Password:", font=('Helvetica', 11))
        password_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))

        password_frame = ttk.Frame(form_frame)
        password_frame.grid(row=2, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=password_var, show="•", width=30)
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add trace to password field for strength checking
        password_var.trace_add("write", lambda *args: self.update_password_strength(
            password_var.get(), strength_meter, strength_label, feedback_label))

        generate_button = ttk.Button(password_frame, text="Generate", width=10,
                                    command=lambda: self.generate_and_set_password(
                                        password_var, strength_meter, strength_label, feedback_label))
        generate_button.pack(side=tk.RIGHT, padx=(5, 0))

        # Password strength meter
        strength_frame = ttk.Frame(form_frame)
        strength_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E, pady=(0, 10))

        strength_meter = ttk.Progressbar(strength_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        strength_meter.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        strength_label = ttk.Label(strength_frame, text="Password Strength: Not Rated", font=('Helvetica', 9))
        strength_label.pack(side=tk.LEFT)

        feedback_label = ttk.Label(strength_frame, text="", font=('Helvetica', 9), foreground='#777777')
        feedback_label.pack(side=tk.TOP, anchor=tk.W, pady=(5, 0))

        # URL
        url_label = ttk.Label(form_frame, text="URL:", font=('Helvetica', 11))
        url_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 10))

        url_var = tk.StringVar()
        url_entry = ttk.Entry(form_frame, textvariable=url_var, width=40)
        url_entry.grid(row=4, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # Notes
        notes_label = ttk.Label(form_frame, text="Notes:", font=('Helvetica', 11))
        notes_label.grid(row=5, column=0, sticky=tk.NW, pady=(0, 10))

        notes_text = tk.Text(form_frame, height=5, width=30, wrap=tk.WORD)
        notes_text.grid(row=5, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))

        cancel_button = ttk.Button(button_frame, text="Cancel",
                                  command=dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=(0, 10))

        save_button = ttk.Button(button_frame, text="Save", style='TButton',
                                command=lambda: self.save_new_password(
                                    service_var.get(), username_var.get(), password_var.get(),
                                    url_var.get(), notes_text.get("1.0", tk.END), dialog))
        save_button.pack(side=tk.RIGHT)

    def update_password_strength(self, password, strength_meter, strength_label, feedback_label):
        """Update the password strength meter based on the current password"""
        if not password:
            strength_meter['value'] = 0
            strength_label.config(text="Password Strength: Not Rated")
            feedback_label.config(text="")
            return

        score, strength_text, feedback = check_password_strength(password)

        # Update progress bar
        strength_meter['value'] = score

        # Update strength label
        strength_label.config(text=f"Password Strength: {strength_text}")

        # Update color based on strength
        if score <= 25:
            strength_meter.configure(style='Red.Horizontal.TProgressbar')
        elif score <= 50:
            strength_meter.configure(style='Orange.Horizontal.TProgressbar')
        elif score <= 75:
            strength_meter.configure(style='Yellow.Horizontal.TProgressbar')
        else:
            strength_meter.configure(style='Green.Horizontal.TProgressbar')

        # Update feedback
        feedback_label.config(text=", ".join(feedback) if feedback else "Good password!")

    def generate_and_set_password(self, password_var, strength_meter, strength_label, feedback_label):
        """Generate a password and update the strength meter"""
        password = self.password_manager.generate_password()
        password_var.set(password)
        self.update_password_strength(password, strength_meter, strength_label, feedback_label)

    def save_new_password(self, service, username, password, url, notes, dialog):
        """Save a new password to the vault"""
        # Validate required fields
        if not service or not username or not password:
            messagebox.showerror("Error", "Service, username, and password are required")
            return

        # Strip trailing newline from notes
        notes = notes.strip()

        # Add password to vault
        success = self.password_manager.add_password(service, username, password, url, notes)

        if success:
            # Close dialog
            dialog.destroy()
            # Refresh password list
            self.load_password_list()
            # Show success message
            messagebox.showinfo("Success", "Password saved successfully")
        else:
            messagebox.showerror("Error", "Failed to save password")

    def edit_password(self, service, username):
        """Show dialog to edit an existing password"""
        # Get existing password data
        password_data = self.password_manager.get_password(service, username)
        if not password_data:
            return

        # Create a new top-level window
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Password")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()  # Make dialog modal

        # Apply the same style
        dialog.configure(background="#F5F5F7")

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Service
        service_label = ttk.Label(form_frame, text="Service:", font=('Helvetica', 11))
        service_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        service_var = tk.StringVar(value=service)
        service_entry = ttk.Entry(form_frame, textvariable=service_var, width=40)
        service_entry.grid(row=0, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # Username
        username_label = ttk.Label(form_frame, text="Username:", font=('Helvetica', 11))
        username_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

        username_var = tk.StringVar(value=username)
        username_entry = ttk.Entry(form_frame, textvariable=username_var, width=40)
        username_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # Password
        password_label = ttk.Label(form_frame, text="Password:", font=('Helvetica', 11))
        password_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))

        password_frame = ttk.Frame(form_frame)
        password_frame.grid(row=2, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        password_var = tk.StringVar(value=password_data["password"])
        password_entry = ttk.Entry(password_frame, textvariable=password_var, show="•", width=30)
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add trace to password field for strength checking
        password_var.trace_add("write", lambda *args: self.update_password_strength(
            password_var.get(), strength_meter, strength_label, feedback_label))

        generate_button = ttk.Button(password_frame, text="Generate", width=10,
                                     command=lambda: self.generate_and_set_password(
                                         password_var, strength_meter, strength_label, feedback_label))
        generate_button.pack(side=tk.RIGHT, padx=(5, 0))

        # Password strength meter
        strength_frame = ttk.Frame(form_frame)
        strength_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E, pady=(0, 10))

        strength_meter = ttk.Progressbar(strength_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        strength_meter.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        strength_label = ttk.Label(strength_frame, text="Password Strength: Not Rated", font=('Helvetica', 9))
        strength_label.pack(side=tk.LEFT)

        feedback_label = ttk.Label(strength_frame, text="", font=('Helvetica', 9), foreground='#777777')
        feedback_label.pack(side=tk.TOP, anchor=tk.W, pady=(5, 0))

        # Initialize strength meter with current password
        self.update_password_strength(password_data["password"], strength_meter, strength_label, feedback_label)

        # URL
        url_label = ttk.Label(form_frame, text="URL:", font=('Helvetica', 11))
        url_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 10))

        url_var = tk.StringVar(value=password_data["url"])
        url_entry = ttk.Entry(form_frame, textvariable=url_var, width=40)
        url_entry.grid(row=4, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # Notes
        notes_label = ttk.Label(form_frame, text="Notes:", font=('Helvetica', 11))
        notes_label.grid(row=5, column=0, sticky=tk.NW, pady=(0, 10))

        notes_text = tk.Text(form_frame, height=5, width=30, wrap=tk.WORD)
        notes_text.grid(row=4, column=1, sticky=tk.W + tk.E, pady=(0, 10))
        notes_text.insert(tk.END, password_data["notes"])

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))

        cancel_button = ttk.Button(button_frame, text="Cancel",
                                   command=dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=(0, 10))

        save_button = ttk.Button(button_frame, text="Save", style='TButton',
                                 command=lambda: self.update_password(
                                     service, username, service_var.get(), username_var.get(),
                                     password_var.get(), url_var.get(), notes_text.get("1.0", tk.END), dialog))
        save_button.pack(side=tk.RIGHT)

    def update_password(self, old_service, old_username, new_service, new_username,
                        new_password, new_url, new_notes, dialog):
        """Update an existing password"""
        # Validate required fields
        if not new_service or not new_username or not new_password:
            messagebox.showerror("Error", "Service, username, and password are required")
            return

        # Strip trailing newline from notes
        new_notes = new_notes.strip()

        # Remove the old password first if service or username changed
        if old_service != new_service or old_username != new_username:
            self.password_manager.remove_password(old_service, old_username)

        # Add/update the password
        success = self.password_manager.add_password(new_service, new_username, new_password, new_url, new_notes)

        if success:
            # Close dialog
            dialog.destroy()
            # Refresh password list
            self.load_password_list()
            # Show success message
            messagebox.showinfo("Success", "Password updated successfully")
        else:
            messagebox.showerror("Error", "Failed to update password")

    def delete_password(self, service, username):
        """Delete a password from the vault"""
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete the password for {service}/{username}?")
        if not confirm:
            return

        # Delete password
        success = self.password_manager.remove_password(service, username)

        if success:
            # Refresh password list
            self.load_password_list()
            # Clear details pane
            self.create_details_pane()
        else:
            messagebox.showerror("Error", "Failed to delete password")

    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Copied to clipboard")

    def toggle_password_visibility(self):
        """Toggle password visibility between hidden and shown"""
        current_value = self.password_var.get()
        if "•" in current_value:
            self.password_var.set(self.real_password)
        else:
            self.password_var.set("•" * len(self.real_password))

    def show_password_details(self, event):
        """Show details of the selected password"""
        self.create_details_pane()

    def generate_password(self):
        """Show dialog to generate a password"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Password")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()  # Make dialog modal

        # Apply the same style
        dialog.configure(background="#F5F5F7")

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Length
        length_label = ttk.Label(form_frame, text="Length:", font=('Helvetica', 11))
        length_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        length_var = tk.IntVar(value=16)
        length_entry = ttk.Entry(form_frame, textvariable=length_var, width=10)
        length_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))

        # Character types
        char_frame = ttk.LabelFrame(form_frame, text="Include Characters", padding="10")
        char_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E, pady=(0, 10))

        # Uppercase
        uppercase_var = tk.BooleanVar(value=True)
        uppercase_check = ttk.Checkbutton(char_frame, text="Uppercase letters (ABC)",
                                          variable=uppercase_var)
        uppercase_check.grid(row=0, column=0, sticky=tk.W, pady=5)

        # Lowercase
        lowercase_var = tk.BooleanVar(value=True)
        lowercase_check = ttk.Checkbutton(char_frame, text="Lowercase letters (abc)",
                                          variable=lowercase_var)
        lowercase_check.grid(row=1, column=0, sticky=tk.W, pady=5)

        # Digits
        digits_var = tk.BooleanVar(value=True)
        digits_check = ttk.Checkbutton(char_frame, text="Digits (123)",
                                       variable=digits_var)
        digits_check.grid(row=2, column=0, sticky=tk.W, pady=5)

        # Special characters
        special_var = tk.BooleanVar(value=True)
        special_check = ttk.Checkbutton(char_frame, text="Special characters (!@#)",
                                        variable=special_var)
        special_check.grid(row=3, column=0, sticky=tk.W, pady=5)

        # Generated password
        password_label = ttk.Label(form_frame, text="Generated Password:", font=('Helvetica', 11))
        password_label.grid(row=2, column=0, sticky=tk.W, pady=(20, 10))

        password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=password_var, width=30)
        password_entry.grid(row=2, column=1, sticky=tk.W + tk.E, pady=(20, 10))

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        generate_button = ttk.Button(button_frame, text="Generate", style='TButton',
                                     command=lambda: self.generate_and_display_password(
                                         length_var.get(), uppercase_var.get(), lowercase_var.get(),
                                         digits_var.get(), special_var.get(), password_var))
        generate_button.pack(side=tk.LEFT, padx=(0, 10))

        copy_button = ttk.Button(button_frame, text="Copy to Clipboard",
                                 command=lambda: self.copy_to_clipboard(password_var.get()))
        copy_button.pack(side=tk.LEFT, padx=(0, 10))

        close_button = ttk.Button(button_frame, text="Close",
                                  command=dialog.destroy)
        close_button.pack(side=tk.LEFT)

        # Generate initial password
        self.generate_and_display_password(
            length_var.get(), uppercase_var.get(), lowercase_var.get(),
            digits_var.get(), special_var.get(), password_var)

    def generate_and_display_password(self, length, include_uppercase, include_lowercase,
                                      include_digits, include_special, password_var):
        """Generate a password based on settings and display it"""
        password = self.password_manager.generate_password(
            length, include_uppercase, include_lowercase, include_digits, include_special)
        password_var.set(password)

    def open_settings(self):
        """Open settings dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()  # Make dialog modal

        # Apply the same style
        dialog.configure(background="#F5F5F7")

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Change master password
        password_frame = ttk.LabelFrame(form_frame, text="Change Master Password", padding="10")
        password_frame.pack(fill=tk.X, pady=(0, 20))

        # Current password
        current_label = ttk.Label(password_frame, text="Current Password:", font=('Helvetica', 11))
        current_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        current_var = tk.StringVar()
        current_entry = ttk.Entry(password_frame, textvariable=current_var, show="•", width=30)
        current_entry.grid(row=0, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # New password
        new_label = ttk.Label(password_frame, text="New Password:", font=('Helvetica', 11))
        new_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

        new_var = tk.StringVar()
        new_entry = ttk.Entry(password_frame, textvariable=new_var, show="•", width=30)
        new_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # Confirm new password
        confirm_label = ttk.Label(password_frame, text="Confirm Password:", font=('Helvetica', 11))
        confirm_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))

        confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(password_frame, textvariable=confirm_var, show="•", width=30)
        confirm_entry.grid(row=2, column=1, sticky=tk.W + tk.E, pady=(0, 10))

        # Change button
        change_button = ttk.Button(password_frame, text="Change Password", style='TButton',
                                   command=lambda: self.change_master_password(
                                       current_var.get(), new_var.get(), confirm_var.get(), dialog))
        change_button.grid(row=3, column=1, sticky=tk.E, pady=(10, 0))

        # Configure grid weights
        password_frame.columnconfigure(1, weight=1)

        # Close button
        close_button = ttk.Button(form_frame, text="Close",
                                  command=dialog.destroy)
        close_button.pack(side=tk.RIGHT, pady=(20, 0))
    '''
    def change_master_password(self, current_password, new_password, confirm_password, dialog):
        """Change the master password"""
        # Validate inputs
        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match")
            return

        # Verify current password
        temp_manager = PasswordManager()
        if not temp_manager.initialize(current_password):
            messagebox.showerror("Error", "Incorrect current password")
            return

        # Change master password
        success = self.password_manager.change_master_password(new_password)
        
        if success:
            dialog.destroy()
            messagebox.showinfo("Success", "Master password changed successfully")
        else:
            messagebox.showerror("Error", "Failed to change master password")
    '''


    def change_master_password(self, current_password, new_password, confirm_password, dialog):
        """Change the master password"""
        # Validate inputs
        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match")
            return

        # Update the password_manager.py change_master_password method according to my previous message
        # Then call it like this:
        success = self.password_manager.change_master_password(current_password, new_password)

        if success:
            dialog.destroy()
            messagebox.showinfo("Success", "Master password changed successfully")
        else:
            messagebox.showerror("Error", "Incorrect current password")

    def lock_vault(self):
        """Lock the vault and return to login screen"""
        # Clear sensitive data
        self.password_manager = PasswordManager()

        # Destroy main interface
        self.main_frame.destroy()

        # Show login screen
        self.create_login_frame()
