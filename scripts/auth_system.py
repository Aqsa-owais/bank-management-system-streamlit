import hashlib
import uuid
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
import json

@dataclass
class User:
    user_id: str
    username: str
    email: str
    password_hash: str
    role: str  # 'admin', 'employee', 'customer'
    full_name: str
    phone: str
    is_active: bool
    created_date: str
    last_login: Optional[str] = None
    customer_id: Optional[str] = None  # Link to customer if role is 'customer'
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def check_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)
    
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    def create_user(cls, username: str, email: str, password: str, role: str, 
                   full_name: str, phone: str, customer_id: str = None):
        return cls(
            user_id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=cls._hash_password(password),
            role=role,
            full_name=full_name,
            phone=phone,
            is_active=True,
            created_date=datetime.now().isoformat(),
            customer_id=customer_id
        )

class AuthSystem:
    def __init__(self, auth_file: str = "users.json"):
        self.auth_file = auth_file
        self.users: Dict[str, User] = {}
        self.load_users()
        self._create_default_admin()
    
    def load_users(self):
        try:
            with open(self.auth_file, 'r') as f:
                data = json.load(f)
                
            for user_data in data.get('users', []):
                user = User.from_dict(user_data)
                self.users[user.username] = user
                
        except FileNotFoundError:
            self.save_users()
        except json.JSONDecodeError:
            print("Error reading auth file. Starting with empty user data.")
    
    def save_users(self):
        data = {
            'users': [user.to_dict() for user in self.users.values()]
        }
        
        with open(self.auth_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _create_default_admin(self):
        """Create default admin user if no admin exists"""
        admin_exists = any(user.role == 'admin' for user in self.users.values())
        
        if not admin_exists:
            admin_user = User.create_user(
                username="admin",
                email="admin@bank.com",
                password="admin123",
                role="admin",
                full_name="System Administrator",
                phone="1234567890"
            )
            self.users["admin"] = admin_user
            self.save_users()
    
    def register_user(self, username: str, email: str, password: str, role: str,
                     full_name: str, phone: str, customer_id: str = None) -> tuple:
        """Register a new user. Returns (success: bool, message: str, user: User or None)"""
        
        # Validate input
        if not all([username, email, password, full_name, phone]):
            return False, "All fields are required", None
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long", None
        
        # Check if username or email already exists
        for user in self.users.values():
            if user.username == username:
                return False, "Username already exists", None
            if user.email == email:
                return False, "Email already exists", None
        
        # Create new user
        try:
            new_user = User.create_user(username, email, password, role, full_name, phone, customer_id)
            self.users[username] = new_user
            self.save_users()
            return True, "User registered successfully", new_user
        except Exception as e:
            return False, f"Error creating user: {str(e)}", None
    
    def login(self, username: str, password: str) -> tuple:
        """Login user. Returns (success: bool, message: str, user: User or None)"""
        
        if username not in self.users:
            return False, "Invalid username or password", None
        
        user = self.users[username]
        
        if not user.is_active:
            return False, "Account is deactivated", None
        
        if not user.check_password(password):
            return False, "Invalid username or password", None
        
        # Update last login
        user.last_login = datetime.now().isoformat()
        self.save_users()
        
        return True, "Login successful", user
    
    def get_user(self, username: str) -> Optional[User]:
        return self.users.get(username)
    
    def get_all_users(self) -> List[User]:
        return list(self.users.values())
    
    def update_user_status(self, username: str, is_active: bool) -> bool:
        if username in self.users:
            self.users[username].is_active = is_active
            self.save_users()
            return True
        return False
    
    def delete_user(self, username: str) -> bool:
        if username in self.users and username != "admin":  # Protect admin user
            del self.users[username]
            self.save_users()
            return True
        return False
    
    def get_users_by_role(self, role: str) -> List[User]:
        return [user for user in self.users.values() if user.role == role]
