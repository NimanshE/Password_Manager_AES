"""
password_manager.py

This module provides the PasswordManager class to manage passwords securely using encryption and decryption with AES-CBC.
The passwords are stored in an encrypted file using AES-CBC encryption with a master password.

Classes:
    PasswordManager: Class to manage passwords securely.

Functions:
    __init__(self, vault_file="password_vault.enc"): Initializes the PasswordManager with the specified vault file.
    initialize(self, master_password): Initializes the password manager with a master password.
    _create_new_vault(self, master_password): Creates a new vault with the given master password.
    _load_vault(self, encrypted_data, master_password): Loads an existing vault using the master password.
    _derive_key(self, password, salt): Derives an encryption key from the password and salt using PBKDF2.
    _encrypt(self, data, key, iv): Encrypts data using AES-CBC.
    _decrypt(self, encrypted_data, key, iv): Decrypts data using AES-CBC.
    _pad(self, data): Pads the data to be a multiple of 16 bytes (AES block size).
    _unpad(self, padded_data): Removes PKCS#7 padding.
    save_vault(self): Saves the vault to the vault file.
    add_password(self, service, username, password=None, url="", notes=""): Adds a new password entry or updates an existing one.
    _get_current_date(self): Gets the current date in a simple format.
    get_password(self, service, username): Retrieves a password.
    remove_password(self, service, username=None): Removes a password entry or all entries for a service.
    get_all_services(self): Gets all services in the vault.
    get_usernames(self, service): Gets all usernames for a specific service.
    generate_password(self, length=16, include_uppercase=True, include_lowercase=True, include_digits=True, include_special=True): Generates a strong random password.
    change_master_password(self, new_master_password): Changes the master password.

Dependencies:
    os: Standard library for interacting with the operating system.
    json: Standard library for JSON serialization and deserialization.
    secrets: Standard library for generating secure random numbers.
    string: Standard library for string operations.
    cryptography: Third-party library for cryptographic operations.
"""

import os
import json
import secrets
import string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class PasswordManager:
    def __init__(self, vault_file="password_vault.enc"):
        self.vault_file = vault_file
        self.master_key = None
        self.vault = {}
        self.salt = None
        self.iv = None
        self.initialized = False

    def initialize(self, master_password):
        """Initialize the password manager with a master password"""
        # Generate salt and derive key from master password
        if os.path.exists(self.vault_file):
            # Load existing vault
            with open(self.vault_file, "rb") as f:
                encrypted_data = f.read()
                if len(encrypted_data) == 0:
                    self._create_new_vault(master_password)
                else:
                    self._load_vault(encrypted_data, master_password)
        else:
            self._create_new_vault(master_password)

    def _create_new_vault(self, master_password):
        """Create a new vault with given master password"""
        # Generate salt and IV
        self.salt = os.urandom(16)
        self.iv = os.urandom(16)

        # Generate key from master password
        self.master_key = self._derive_key(master_password, self.salt)

        # Initialize empty vault
        self.vault = {}
        self.initialized = True

        # Save the vault
        self.save_vault()

    def _load_vault(self, encrypted_data, master_password):
        """Load an existing vault using the master password"""
        try:
            # Extract salt and IV
            salt_iv = encrypted_data[:32]
            self.salt = salt_iv[:16]
            self.iv = salt_iv[16:32]

            # Generate key from master password
            self.master_key = self._derive_key(master_password, self.salt)

            # Decrypt the vault
            cipher_text = encrypted_data[32:]
            decrypted_data = self._decrypt(cipher_text, self.master_key, self.iv)

            # Parse JSON
            self.vault = json.loads(decrypted_data.decode('utf-8'))
            self.initialized = True
            return True
        except Exception as e:
            self.initialized = False
            return False


    def _derive_key(self, password, salt):
        """Derive encryption key from password and salt using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits for AES-256
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def _encrypt(self, data, key, iv):
        """Encrypt data using AES-CBC"""
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad the data to be multiple of 16 bytes (AES block size)
        padded_data = self._pad(data)

        # Encrypt the padded data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted_data

    def _decrypt(self, encrypted_data, key, iv):
        """Decrypt data using AES-CBC"""
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the data
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding
        return self._unpad(padded_data)

    def _pad(self, data):
        """PKCS#7 padding"""
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _unpad(self, padded_data):
        """Remove PKCS#7 padding"""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]

    def save_vault(self):
        """Save the vault to the vault file"""
        if not self.initialized:
            return False

        try:
            # Convert vault to JSON
            vault_json = json.dumps(self.vault).encode('utf-8')

            # Encrypt vault data
            encrypted_data = self._encrypt(vault_json, self.master_key, self.iv)

            # Save salt, IV, and encrypted data
            with open(self.vault_file, "wb") as f:
                f.write(self.salt + self.iv + encrypted_data)

            return True
        except Exception:
            return False

    def add_password(self, service, username, password=None, url="", notes=""):
        """Add a new password entry or update an existing one"""
        if not self.initialized:
            return False

        if password is None:
            password = self.generate_password()

        # Create or update entry
        if service not in self.vault:
            self.vault[service] = {}

        self.vault[service][username] = {
            "password": password,
            "url": url,
            "notes": notes,
            "date_modified": self._get_current_date()
        }

        return self.save_vault()

    def _get_current_date(self):
        """Get current date in simple format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def get_password(self, service, username):
        """Retrieve a password"""
        if not self.initialized:
            return None

        if service in self.vault and username in self.vault[service]:
            return self.vault[service][username]
        else:
            return None

    def remove_password(self, service, username=None):
        """Remove a password entry or all entries for a service"""
        if not self.initialized:
            return False

        if service in self.vault:
            if username is None:
                # Remove all entries for the service
                del self.vault[service]
            elif username in self.vault[service]:
                # Remove specific entry
                del self.vault[service][username]
                if not self.vault[service]:  # If no more usernames for this service
                    del self.vault[service]
            else:
                return False
            return self.save_vault()
        else:
            return False

    def get_all_services(self):
        """Get all services in the vault"""
        if not self.initialized:
            return []

        return sorted(self.vault.keys())

    def get_usernames(self, service):
        """Get all usernames for a specific service"""
        if not self.initialized or service not in self.vault:
            return []

        return sorted(self.vault[service].keys())

    def generate_password(self, length=16, include_uppercase=True, include_lowercase=True,
                          include_digits=True, include_special=True):
        """Generate a strong random password"""
        # Define character sets
        chars = ""
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += string.punctuation

        if not chars:
            chars = string.ascii_letters + string.digits + string.punctuation

        # Generate password
        return ''.join(secrets.choice(chars) for _ in range(length))

    '''def change_master_password(self, new_master_password):
        """Change the master password"""
        if not self.initialized:
            return False

        # Generate new salt and derive new key
        self.salt = os.urandom(16)
        self.master_key = self._derive_key(new_master_password, self.salt)

        return self.save_vault()
    '''

    def change_master_password(self, current_password, new_master_password):
        """Change the master password"""
        if not self.initialized:
            return False

        try:
            # Verify current password by deriving a key and comparing
            test_key = self._derive_key(current_password, self.salt)

            # Compare with current master key - they should match if current_password is correct
            if not self._secure_compare(test_key, self.master_key):
                return False  # Password verification failed

            # Generate new salt and derive new key
            new_salt = os.urandom(16)
            new_key = self._derive_key(new_master_password, new_salt)

            # Save old values in case we need to restore
            old_salt = self.salt
            old_key = self.master_key

            # Update values
            self.salt = new_salt
            self.master_key = new_key

            # Save the vault with new credentials
            if self.save_vault():
                return True
            else:
                # Restore old values if save fails
                self.salt = old_salt
                self.master_key = old_key
                return False
        except Exception:
            return False

    def _secure_compare(self, a, b):
        """Compare two byte strings securely"""
        return secrets.compare_digest(a, b)