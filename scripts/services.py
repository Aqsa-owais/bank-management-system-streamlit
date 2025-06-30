from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
import json
from scripts.models import Customer, User, Account, Transaction

# Abstract Service Classes
class DataService(ABC):
    """Abstract base class for data services"""
    
    @abstractmethod
    def save_data(self):
        """Save data to storage"""
        pass
    
    @abstractmethod
    def load_data(self):
        """Load data from storage"""
        pass

class AuthenticationService(ABC):
    """Abstract base class for authentication services"""
    
    @abstractmethod
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """Authenticate user login"""
        pass
    
    @abstractmethod
    def register_user(self, **kwargs) -> Tuple[bool, str, Optional[User]]:
        """Register new user"""
        pass

class BankingService(ABC):
    """Abstract base class for banking services"""
    
    @abstractmethod
    def create_customer(self, **kwargs) -> Customer:
        """Create new customer"""
        pass
    
    @abstractmethod
    def create_account(self, **kwargs) -> Account:
        """Create new account"""
        pass
    
    @abstractmethod
    def transfer_funds(self, **kwargs) -> Tuple[Transaction, Transaction]:
        """Transfer funds between accounts"""
        pass

# Concrete Service Implementations
class JSONDataService(DataService):
    """JSON file-based data service"""
    
    def __init__(self, filename: str):
        self._filename = filename
        self._data = {}
    
    def save_data(self, data: Dict):
        """Save data to JSON file"""
        with open(self._filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self) -> Dict:
        """Load data from JSON file"""
        try:
            with open(self._filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(f"Error reading {self._filename}. Starting with empty data.")
            return {}

class UserAuthService(AuthenticationService):
    """User authentication service"""
    
    def __init__(self, data_service: DataService, auth_file: str = "users.json"):
        self._data_service = JSONDataService(auth_file)
        self._users: Dict[str, User] = {}
        self._load_users()
        self._create_default_admin()
    
    def _load_users(self):
        """Load users from storage"""
        data = self._data_service.load_data()
        for user_data in data.get('users', []):
            user = User.from_dict(user_data)
            self._users[user.username] = user
    
    def _save_users(self):
        """Save users to storage"""
        data = {'users': [user.to_dict() for user in self._users.values()]}
        self._data_service.save_data(data)
    
    def _create_default_admin(self):
        """Create default admin user if none exists"""
        admin_exists = any(user.role == 'admin' for user in self._users.values())
        if not admin_exists:
            admin_user = User.create_user(
                username="admin",
                email="admin@bank.com",
                password="admin123",
                role="admin",
                full_name="System Administrator",
                phone="1234567890"
            )
            self._users["admin"] = admin_user
            self._save_users()
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """Authenticate user login"""
        if username not in self._users:
            return False, "Invalid username or password", None
        
        user = self._users[username]
        if not user.is_active:
            return False, "Account is deactivated", None
        
        if not user.check_password(password):
            return False, "Invalid username or password", None
        
        user.update_last_login()
        self._save_users()
        return True, "Login successful", user
    
    def register_user(self, username: str, email: str, password: str, role: str,
                     full_name: str, phone: str, customer_id: str = None) -> Tuple[bool, str, Optional[User]]:
        """Register new user"""
        if not all([username, email, password, full_name, phone]):
            return False, "All fields are required", None
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long", None
        
        for user in self._users.values():
            if user.username == username:
                return False, "Username already exists", None
            if user.email == email:
                return False, "Email already exists", None
        
        try:
            new_user = User.create_user(username, email, password, role, full_name, phone, customer_id)
            self._users[username] = new_user
            self._save_users()
            return True, "User registered successfully", new_user
        except Exception as e:
            return False, f"Error creating user: {str(e)}", None
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self._users.get(username)
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return list(self._users.values())
    
    def update_user_status(self, username: str, is_active: bool) -> bool:
        """Update user status"""
        if username in self._users:
            self._users[username].set_active_status(is_active)
            self._save_users()
            return True
        return False
    
    def delete_user(self, username: str) -> bool:
        """Delete user"""
        if username in self._users and username != "admin":
            del self._users[username]
            self._save_users()
            return True
        return False

class BankManagementService(BankingService):
    """Main banking service"""
    
    def __init__(self, data_file: str = "bank_data.json"):
        self._data_service = JSONDataService(data_file)
        self._customers: Dict[str, Customer] = {}
        self._accounts: Dict[str, Account] = {}
        self._auth_service = UserAuthService(self._data_service)
        self._load_data()
    
    @property
    def auth_service(self) -> UserAuthService:
        """Get authentication service"""
        return self._auth_service
    
    def _load_data(self):
        """Load banking data"""
        data = self._data_service.load_data()
        
        # Load customers
        for customer_data in data.get('customers', []):
            customer = Customer.from_dict(customer_data)
            self._customers[customer.id] = customer
        
        # Load accounts
        for account_data in data.get('accounts', []):
            account = Account.from_dict(account_data)
            self._accounts[account.id] = account
            
            # Link account to customer
            if account.customer_id in self._customers:
                self._customers[account.customer_id].add_account(account)
    
    def _save_data(self):
        """Save banking data"""
        data = {
            'customers': [customer.to_dict() for customer in self._customers.values()],
            'accounts': [account.to_dict() for account in self._accounts.values()]
        }
        self._data_service.save_data(data)
    
    def create_customer(self, name: str, email: str, phone: str, address: str) -> Customer:
        """Create new customer"""
        import uuid
        customer_id = str(uuid.uuid4())
        customer = Customer(customer_id, name, email, phone, address)
        self._customers[customer_id] = customer
        self._save_data()
        return customer
    
    def create_account(self, customer_id: str, account_type: str, initial_deposit: float = 0.0) -> Account:
        """Create new account"""
        if customer_id not in self._customers:
            raise ValueError("Customer not found")
        
        account_id = f"ACC{len(self._accounts) + 1:06d}"
        account = Account(account_id, customer_id, account_type, initial_deposit)
        
        if initial_deposit > 0:
            account.deposit(initial_deposit, "Initial deposit")
        
        self._accounts[account_id] = account
        self._customers[customer_id].add_account(account)
        self._save_data()
        return account
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        return self._customers.get(customer_id)
    
    def get_account(self, account_id: str) -> Optional[Account]:
        """Get account by ID"""
        return self._accounts.get(account_id)
    
    def get_customer_accounts(self, customer_id: str) -> List[Account]:
        """Get all accounts for a customer"""
        return [account for account in self._accounts.values() 
                if account.customer_id == customer_id]
    
    def transfer_funds(self, from_account_id: str, to_account_id: str, 
                      amount: float, description: str = "Transfer") -> Tuple[Transaction, Transaction]:
        """Transfer funds between accounts"""
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        
        if not from_account or not to_account:
            raise ValueError("One or both accounts not found")
        
        if from_account.balance < amount:
            raise ValueError("Insufficient funds")
        
        # Create transfer transactions
        import uuid
        from_transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=from_account_id,
            transaction_type="transfer_out",
            amount=amount,
            balance_after=from_account.balance - amount,
            description=f"Transfer to {to_account_id}: {description}",
            reference_account=to_account_id
        )
        
        to_transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=to_account_id,
            transaction_type="transfer_in",
            amount=amount,
            balance_after=to_account.balance + amount,
            description=f"Transfer from {from_account_id}: {description}",
            reference_account=from_account_id
        )
        
        # Update balances
        from_account._balance -= amount
        to_account._balance += amount
        
        # Add transactions
        from_account.add_transaction(from_transaction)
        to_account.add_transaction(to_transaction)
        
        self._save_data()
        return from_transaction, to_transaction
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return list(self._customers.values())
    
    def get_all_accounts(self) -> List[Account]:
        """Get all accounts"""
        return list(self._accounts.values())
    
    def get_bank_summary(self) -> Dict:
        """Get bank summary statistics"""
        total_customers = len(self._customers)
        total_accounts = len(self._accounts)
        total_balance = sum(account.balance for account in self._accounts.values())
        active_accounts = len([acc for acc in self._accounts.values() if acc.status == 'active'])
        
        return {
            'total_customers': total_customers,
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'total_balance': total_balance
        }
