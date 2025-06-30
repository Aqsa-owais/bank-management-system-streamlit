import json
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import uuid
from scripts.auth_system import AuthSystem, User

@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str
    address: str
    created_date: str
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    transaction_type: str  # 'deposit', 'withdraw', 'transfer_in', 'transfer_out'
    amount: float
    balance_after: float
    description: str
    timestamp: str
    reference_account: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class Account:
    def __init__(self, account_id: str, customer_id: str, account_type: str, 
                 balance: float = 0.0, status: str = "active", created_date: str = None):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_type = account_type  # 'savings', 'checking', 'business'
        self.balance = balance
        self.status = status  # 'active', 'inactive', 'frozen'
        self.created_date = created_date or datetime.datetime.now().isoformat()
        self.transactions: List[Transaction] = []
    
    def deposit(self, amount: float, description: str = "Deposit") -> Transaction:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=self.account_id,
            transaction_type="deposit",
            amount=amount,
            balance_after=self.balance,
            description=description,
            timestamp=datetime.datetime.now().isoformat()
        )
        self.transactions.append(transaction)
        return transaction
    
    def withdraw(self, amount: float, description: str = "Withdrawal") -> Transaction:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=self.account_id,
            transaction_type="withdraw",
            amount=amount,
            balance_after=self.balance,
            description=description,
            timestamp=datetime.datetime.now().isoformat()
        )
        self.transactions.append(transaction)
        return transaction
    
    def get_transaction_history(self, limit: int = None) -> List[Transaction]:
        transactions = sorted(self.transactions, key=lambda x: x.timestamp, reverse=True)
        return transactions[:limit] if limit else transactions
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'customer_id': self.customer_id,
            'account_type': self.account_type,
            'balance': self.balance,
            'status': self.status,
            'created_date': self.created_date,
            'transactions': [t.to_dict() for t in self.transactions]
        }
    
    @classmethod
    def from_dict(cls, data):
        account = cls(
            account_id=data['account_id'],
            customer_id=data['customer_id'],
            account_type=data['account_type'],
            balance=data['balance'],
            status=data['status'],
            created_date=data['created_date']
        )
        account.transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
        return account

class BankSystem:
    def __init__(self, data_file: str = "bank_data.json"):
        self.data_file = data_file
        self.customers: Dict[str, Customer] = {}
        self.accounts: Dict[str, Account] = {}
        self.auth_system = AuthSystem()  # Add this line
        self.load_data()
    
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
            # Load customers
            for customer_data in data.get('customers', []):
                customer = Customer.from_dict(customer_data)
                self.customers[customer.customer_id] = customer
            
            # Load accounts
            for account_data in data.get('accounts', []):
                account = Account.from_dict(account_data)
                self.accounts[account.account_id] = account
                
        except FileNotFoundError:
            # Initialize with empty data
            self.save_data()
        except json.JSONDecodeError:
            print("Error reading data file. Starting with empty data.")
    
    def save_data(self):
        data = {
            'customers': [customer.to_dict() for customer in self.customers.values()],
            'accounts': [account.to_dict() for account in self.accounts.values()]
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_customer(self, name: str, email: str, phone: str, address: str) -> Customer:
        customer_id = str(uuid.uuid4())
        customer = Customer(
            customer_id=customer_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            created_date=datetime.datetime.now().isoformat()
        )
        self.customers[customer_id] = customer
        self.save_data()
        return customer
    
    def create_account(self, customer_id: str, account_type: str, initial_deposit: float = 0.0) -> Account:
        if customer_id not in self.customers:
            raise ValueError("Customer not found")
        
        account_id = f"ACC{len(self.accounts) + 1:06d}"
        account = Account(
            account_id=account_id,
            customer_id=customer_id,
            account_type=account_type,
            balance=initial_deposit
        )
        
        if initial_deposit > 0:
            account.deposit(initial_deposit, "Initial deposit")
        
        self.accounts[account_id] = account
        self.save_data()
        return account
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        return self.customers.get(customer_id)
    
    def get_account(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)
    
    def get_customer_accounts(self, customer_id: str) -> List[Account]:
        return [account for account in self.accounts.values() 
                if account.customer_id == customer_id]
    
    def transfer_funds(self, from_account_id: str, to_account_id: str, 
                      amount: float, description: str = "Transfer") -> tuple:
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        
        if not from_account or not to_account:
            raise ValueError("One or both accounts not found")
        
        if from_account.balance < amount:
            raise ValueError("Insufficient funds")
        
        # Perform transfer
        from_transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=from_account_id,
            transaction_type="transfer_out",
            amount=amount,
            balance_after=from_account.balance - amount,
            description=f"Transfer to {to_account_id}: {description}",
            timestamp=datetime.datetime.now().isoformat(),
            reference_account=to_account_id
        )
        
        to_transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=to_account_id,
            transaction_type="transfer_in",
            amount=amount,
            balance_after=to_account.balance + amount,
            description=f"Transfer from {from_account_id}: {description}",
            timestamp=datetime.datetime.now().isoformat(),
            reference_account=from_account_id
        )
        
        from_account.balance -= amount
        to_account.balance += amount
        
        from_account.transactions.append(from_transaction)
        to_account.transactions.append(to_transaction)
        
        self.save_data()
        return from_transaction, to_transaction
    
    def get_all_customers(self) -> List[Customer]:
        return list(self.customers.values())
    
    def get_all_accounts(self) -> List[Account]:
        return list(self.accounts.values())
    
    def get_bank_summary(self) -> Dict:
        total_customers = len(self.customers)
        total_accounts = len(self.accounts)
        total_balance = sum(account.balance for account in self.accounts.values())
        active_accounts = len([acc for acc in self.accounts.values() if acc.status == 'active'])
        
        return {
            'total_customers': total_customers,
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'total_balance': total_balance
        }

    def link_customer_to_user(self, customer_id: str, user_id: str):
        """Link a customer to a user account"""
        if customer_id in self.customers:
            user = self.auth_system.get_user_by_id(user_id)
            if user:
                user.customer_id = customer_id
                self.auth_system.save_users()
                return True
        return False
