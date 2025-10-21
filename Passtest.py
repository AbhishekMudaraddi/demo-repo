import os
import json
import base64
import secrets
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class SecurePasswordManager:
    def __init__(self):
        self.users = {}
        self.db_file = "secure_password_db.json"
        self.load_database()
    
    def load_database(self):
        try:
            with open(self.db_file, 'r') as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}
    
    def save_database(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f)
    
    def generate_salt(self, length=16):
        """Generate a cryptographically secure random salt"""
        return os.urandom(length)
    
    def derive_key(self, password, salt, iterations=100000):
        """Derive an encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit key
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        return kdf.derive(password.encode())
    
    def encrypt_data(self, data, key):
        """Encrypt data using AES-GCM"""
        iv = os.urandom(16)  # Initialization vector
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return iv + encryptor.tag + encrypted_data
    
    def decrypt_data(self, encrypted_data, key):
        """Decrypt data using AES-GCM"""
        iv = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
    
    def create_account(self, username, master_password):
        """Create a new user account with recovery codes"""
        if username in self.users:
            return False, "Username already exists", []
        
        # Generate salt for key derivation
        salt = self.generate_salt()
        
        # Derive encryption key from master password
        encryption_key = self.derive_key(master_password, salt)
        
        # Generate a random master key for encrypting passwords
        master_key = os.urandom(32)
        
        # Encrypt the master key with the derived key
        encrypted_master_key = self.encrypt_data(master_key, encryption_key)
        
        # Generate recovery codes
        recovery_codes = []
        recovery_data = []
        for _ in range(10):
            code = ''.join(secrets.choice("0123456789") for _ in range(8))
            recovery_codes.append(code)
            
            # Generate a salt for this recovery code
            recovery_salt = self.generate_salt()
            
            # Derive a key from the recovery code
            recovery_key = self.derive_key(code, recovery_salt)
            
            # Encrypt the master key with the recovery key
            encrypted_key = self.encrypt_data(master_key, recovery_key)
            
            recovery_data.append({
                'salt': base64.b64encode(recovery_salt).decode('ascii'),
                'encrypted_key': base64.b64encode(encrypted_key).decode('ascii')
            })
        
        # Store user data
        self.users[username] = {
            'salt': base64.b64encode(salt).decode('ascii'),
            'encrypted_master_key': base64.b64encode(encrypted_master_key).decode('ascii'),
            'passwords': {},
            'recovery_data': recovery_data
        }
        
        self.save_database()
        return True, "Account created successfully", recovery_codes
    
    def login(self, username, master_password):
        """Verify user credentials and return master key"""
        if username not in self.users:
            return False, "User not found", None
        
        user_data = self.users[username]
        
        # Get salt and decode it
        salt = base64.b64decode(user_data['salt'].encode('ascii'))
        
        # Re-derive the encryption key
        encryption_key = self.derive_key(master_password, salt)
        
        # Get and decode the encrypted master key
        encrypted_master_key = base64.b64decode(user_data['encrypted_master_key'].encode('ascii'))
        
        # Decrypt the master key
        try:
            master_key = self.decrypt_data(encrypted_master_key, encryption_key)
            return True, "Login successful", master_key
        except:
            return False, "Invalid password", None
    
    def add_password(self, username, master_password, service, password):
        """Add a password for a service"""
        if username not in self.users:
            return False, "User not found"
        
        # Verify login and get master key
        success, message, master_key = self.login(username, master_password)
        if not success:
            return success, message
        
        # Encrypt the password with the master key
        encrypted_password = self.encrypt_data(password.encode(), master_key)
        
        # Store the encrypted password
        self.users[username]['passwords'][service] = base64.b64encode(encrypted_password).decode('ascii')
        self.save_database()
        return True, f"Password for {service} added successfully"
    
    def get_password(self, username, master_password, service):
        """Retrieve a password for a service"""
        if username not in self.users:
            return False, "User not found", None
        
        # Verify login and get master key
        success, message, master_key = self.login(username, master_password)
        if not success:
            return success, message, None
        
        user_data = self.users[username]
        
        if service not in user_data['passwords']:
            return False, f"No password stored for {service}", None
        
        # Get and decode the encrypted password
        encrypted_password = base64.b64decode(user_data['passwords'][service].encode('ascii'))
        
        # Decrypt the password
        try:
            decrypted_password = self.decrypt_data(encrypted_password, master_key)
            return True, f"Password for {service}", decrypted_password.decode()
        except:
            return False, "Failed to decrypt password", None
    
    def recover_account(self, username, recovery_code, new_master_password):
        """Recover account using a recovery code"""
        if username not in self.users:
            return False, "User not found", None
        
        user_data = self.users[username]
        
        # Try each recovery code
        for recovery_entry in user_data['recovery_data']:
            # Get and decode the recovery salt
            recovery_salt = base64.b64decode(recovery_entry['salt'].encode('ascii'))
            
            # Derive a key from the recovery code
            recovery_key = self.derive_key(recovery_code, recovery_salt)
            
            # Get and decode the encrypted master key
            encrypted_key = base64.b64decode(recovery_entry['encrypted_key'].encode('ascii'))
            
            # Try to decrypt the master key
            try:
                master_key = self.decrypt_data(encrypted_key, recovery_key)
                
                # If we get here, the recovery code was valid
                # Now set a new master password
                
                # Generate a new salt
                new_salt = self.generate_salt()
                
                # Derive a new encryption key from the new master password
                new_encryption_key = self.derive_key(new_master_password, new_salt)
                
                # Encrypt the master key with the new encryption key
                new_encrypted_master_key = self.encrypt_data(master_key, new_encryption_key)
                
                # Update the user data
                user_data['salt'] = base64.b64encode(new_salt).decode('ascii')
                user_data['encrypted_master_key'] = base64.b64encode(new_encrypted_master_key).decode('ascii')
                
                # Remove the used recovery code
                user_data['recovery_data'].remove(recovery_entry)
                
                self.save_database()
                return True, "Account recovered successfully", master_key
            except:
                # This recovery code didn't match, try the next one
                continue
        
        # If we get here, no valid recovery code was found
        return False, "Invalid recovery code", None


# Interactive console for testing
def test_secure_manager():
    manager = SecurePasswordManager()
    
    print("=== Secure Password Manager ===")
    print("1. Create Account")
    print("2. Login")
    print("3. Add Password")
    print("4. Get Password")
    print("5. Recover Account")
    print("6. Exit")
    
    while True:
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter master password: ")
            success, message, recovery_codes = manager.create_account(username, password)
            print(message)
            if success:
                print("Recovery Codes (save these in a secure place):")
                for i, code in enumerate(recovery_codes, 1):
                    print(f"{i}. {code}")
        
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter master password: ")
            success, message, _ = manager.login(username, password)
            print(message)
        
        elif choice == "3":
            username = input("Enter username: ")
            password = input("Enter master password: ")
            service = input("Enter service name: ")
            service_password = input(f"Enter password for {service}: ")
            success, message = manager.add_password(username, password, service, service_password)
            print(message)
        
        elif choice == "4":
            username = input("Enter username: ")
            password = input("Enter master password: ")
            service = input("Enter service name: ")
            success, message, password = manager.get_password(username, password, service)
            if success:
                print(f"{message}: {password}")
            else:
                print(message)
        
        elif choice == "5":
            username = input("Enter username: ")
            recovery_code = input("Enter recovery code: ")
            new_password = input("Enter new master password: ")
            success, message, _ = manager.recover_account(username, recovery_code, new_password)
            print(message)
        
        elif choice == "6":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    test_secure_manager()


    # this is the sample test that i am usimg to see that the changes will be there in the git or no 