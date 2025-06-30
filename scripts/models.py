from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import uuid
import json
import hashlib

# Abstract Base Classes for OOP Structure
class Serializable(ABC):
    """Abstract base class for serializable objects"""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dictionary"""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create object from dictionary"""
        pass

class Identifiable(ABC):
    """Abstract base class for objects with unique identifiers"""
    
    @property
    @abstractmethod
    def id(self) -> str:
        """Get unique identifier"""
        pass

class Timestamped(ABC):
    """Abstract base class for objects with timestamps"""
    
    @property
    @abstractmethod
    def created_at(self) -> str:
        """Get creation timestamp"""
        pass

# Core Model Classes
class Person(Serializable, Identifiable, Timestamped):
    """Base class for all person entities"""
    
    def __init__(self, person_id: str, name: str, email: str, phone: str, created_date: str = None):
        self._id = person_id
        self._name = name
        self._email = email
        self._phone = phone
        self._created_date = created_date or datetime.now().isoformat()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @property
    def created_at(self) -> str:
        return self._created_date
    
    def update_contact_info(self, email: str = None, phone: str = None):
        """Update contact information"""
        if email:
            self._email = email
        if phone:
            self._phone = phone

class Customer(Person):
    """Customer class inheriting from Person"""
    
    def __init__(self, customer_id: str, name: str, email: str, phone: str, address: str, created_date: str = None):
        super().__init__(customer_id, name, email, phone, created_date)
        self._address = address
        self._accounts: List['Account'] = []
    
    @property
    def address(self) -> str:
        return self._address
    
    @property
    def accounts(self) -> List['Account']:
        return self._accounts.copy()
    
    def add_account(self, account: 'Account'):
        """Add an account to customer"""
        if account not in self._accounts:
            self._accounts.append(account)
    
    def remove_account(self, account: 'Account'):
        """Remove an account from customer"""
        if account in self._accounts:
            self._accounts.remove(account)
    
    def get_total_balance(self) -> float:
        """Get total balance across all accounts"""
        return sum(account.balance for account in self._accounts)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'customer_id': self._id,
            'name': self._name,
            'email': self._email,
            'phone': self._phone,
            'address': self._address,
            'created_date': self._created_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            customer_id=data['customer_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            created_date=data.get('created_date')
        )

class User(Person):
    """User class for authentication"""
    
    def __init__(self, user_id: str, username: str, email: str, password_hash: str, 
                 role: str, full_name: str, phone: str, is_active: bool = True, 
                 created_date: str = None, last_login: str = None, customer_id: str = None):
        super().__init__(user_id, full_name, email, phone, created_date)
        self._username = username
        self._password_hash = password_hash
        self._role = role
        self._is_active = is_active
        self._last_login = last_login
        self._customer_id = customer_id
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def role(self) -> str:
        return self._role
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @property
    def last_login(self) -> Optional[str]:
        return self._last_login
    
    @property
    def customer_id(self) -> Optional[str]:
        return self._customer_id
    
    def set_active_status(self, status: bool):
        """Set user active status"""
        self._is_active = status
    
    def update_last_login(self):
        """Update last login timestamp"""
        self._last_login = datetime.now().isoformat()
    
    def check_password(self, password: str) -> bool:
        """Check if password matches"""
        return self._password_hash == self._hash_password(password)
    
    def change_password(self, new_password: str):
        """Change user password"""
        self._password_hash = self._hash_password(new_password)
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    def create_user(cls, username: str, email: str, password: str, role: str, 
                   full_name: str, phone: str, customer_id: str = None):
        """Factory method to create a new user"""
        return cls(
            user_id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=cls._hash_password(password),
            role=role,
            full_name=full_name,
            phone=phone,
            customer_id=customer_id
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self._id,
            'username': self._username,
            'email': self._email,
            'password_hash': self._password_hash,
            'role': self._role,
            'full_name': self._name,
            'phone': self._phone,
            'is_active': self._is_active,
            'created_date': self._created_date,
            'last_login': self._last_login,
            'customer_id': self._customer_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            role=data['role'],
            full_name=data['full_name'],
            phone=data['phone'],
            is_active=data.get('is_active', True),
            created_date=data.get('created_date'),
            last_login=data.get('last_login'),
            customer_id=data.get('customer_id')
        )

class Transaction(Serializable, Identifiable, Timestamped):
    """Transaction class for banking operations"""
    
    def __init__(self, transaction_id: str, account_id: str, transaction_type: str, 
                 amount: float, balance_after: float, description: str, 
                 timestamp: str = None, reference_account: str = None):
        self._id = transaction_id
        self._account_id = account_id
        self._type = transaction_type
        self._amount = amount
        self._balance_after = balance_after
        self._description = description
        self._timestamp = timestamp or datetime.now().isoformat()
        self._reference_account = reference_account
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def account_id(self) -> str:
        return self._account_id
    
    @property
    def transaction_type(self) -> str:
        return self._type
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def balance_after(self) -> float:
        return self._balance_after
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def created_at(self) -> str:
        return self._timestamp
    
    @property
    def reference_account(self) -> Optional[str]:
        return self._reference_account
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'transaction_id': self._id,
            'account_id': self._account_id,
            'transaction_type': self._type,
            'amount': self._amount,
            'balance_after': self._balance_after,
            'description': self._description,
            'timestamp': self._timestamp,
            'reference_account': self._reference_account
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            transaction_id=data['transaction_id'],
            account_id=data['account_id'],
            transaction_type=data['transaction_type'],
            amount=data['amount'],
            balance_after=data['balance_after'],
            description=data['description'],
            timestamp=data.get('timestamp'),
            reference_account=data.get('reference_account')
        )

class Account(Serializable, Identifiable, Timestamped):
    """Account class for banking accounts"""
    
    def __init__(self, account_id: str, customer_id: str, account_type: str, 
                 balance: float = 0.0, status: str = "active", created_date: str = None):
        self._id = account_id
        self._customer_id = customer_id
        self._type = account_type
        self._balance = balance
        self._status = status
        self._created_date = created_date or datetime.now().isoformat()
        self._transactions: List[Transaction] = []
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def customer_id(self) -> str:
        return self._customer_id
    
    @property
    def account_type(self) -> str:
        return self._type
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def created_at(self) -> str:
        return self._created_date
    
    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions.copy()
    
    def set_status(self, status: str):
        """Set account status"""
        valid_statuses = ["active", "inactive", "frozen"]
        if status in valid_statuses:
            self._status = status
        else:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
    
    def deposit(self, amount: float, description: str = "Deposit") -> Transaction:
        """Make a deposit to the account"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount
        transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=self._id,
            transaction_type="deposit",
            amount=amount,
            balance_after=self._balance,
            description=description
        )
        self._transactions.append(transaction)
        return transaction
    
    def withdraw(self, amount: float, description: str = "Withdrawal") -> Transaction:
        """Make a withdrawal from the account"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        
        self._balance -= amount
        transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=self._id,
            transaction_type="withdraw",
            amount=amount,
            balance_after=self._balance,
            description=description
        )
        self._transactions.append(transaction)
        return transaction
    
    def add_transaction(self, transaction: Transaction):
        """Add a transaction to the account"""
        self._transactions.append(transaction)
    
    def get_transaction_history(self, limit: int = None) -> List[Transaction]:
        """Get transaction history"""
        sorted_transactions = sorted(self._transactions, key=lambda x: x.created_at, reverse=True)
        return sorted_transactions[:limit] if limit else sorted_transactions
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self._id,
            'customer_id': self._customer_id,
            'account_type': self._type,
            'balance': self._balance,
            'status': self._status,
            'created_date': self._created_date,
            'transactions': [t.to_dict() for t in self._transactions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        account = cls(
            account_id=data['account_id'],
            customer_id=data['customer_id'],
            account_type=data['account_type'],
            balance=data['balance'],
            status=data['status'],
            created_date=data['created_date']
        )
        account._transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
        return account
