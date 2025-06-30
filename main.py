import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from scripts.services import BankManagementService
from scripts.models import Customer, Account
from pages.auth_pages import create_auth_ui

# Page configuration
st.set_page_config(
    page_title="Professional Bank Management System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Clean Design
st.markdown("""
<style>
    /* Professional Color Variables */
    :root {
        --primary-blue: #0079bf;
        --hover-blue: #329cf7;
        --light-grey: #bac5cc;
        --white: #ffffff;
        --text-dark: #2c3e50;
        --text-light: #7f8c8d;
        --border-light: #e8ecef;
        --shadow-light: rgba(0, 121, 191, 0.08);
        --shadow-medium: rgba(0, 121, 191, 0.12);
    }

    /* Global Styling */
    .main .block-container {
        background: #ffffff;
        padding: 2rem;
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Professional Header */
    .main-header {
        background: #0079bf;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px var(--shadow-light);
    }

    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-weight: 600;
        font-size: 2.2rem;
        letter-spacing: -0.5px;
    }

    /* Professional Cards */
    .metric-card, .dashboard-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px var(--shadow-light);
        border: 1px solid var(--border-light);
        margin: 1rem 0;
        transition: all 0.2s ease;
    }

    .dashboard-card:hover {
        box-shadow: 0 4px 12px var(--shadow-medium);
        border-color: var(--hover-blue);
        transform: translateY(-1px);
    }

    .dashboard-card h3 {
        color: var(--primary-blue);
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .dashboard-card h2 {
        color: var(--text-dark);
        font-weight: 700;
        margin: 0;
        font-size: 1.8rem;
    }

    /* User Info Card */
    .user-info {
        background: var(--primary-blue);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px var(--shadow-light);
        text-align: center;
    }

    .user-info strong {
        font-size: 1.1rem;
        font-weight: 600;
    }

    .user-info small {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* Professional Buttons */
    .stButton > button {
        background: var(--primary-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px var(--shadow-light) !important;
    }

    .stButton > button:hover {
        background: var(--hover-blue) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px var(--shadow-medium) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: var(--primary-blue) !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--hover-blue) !important;
    }

    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border: 1px solid var(--light-grey) !important;
        border-radius: 6px !important;
        background: white !important;
        padding: 0.7rem !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        color: var(--text-dark) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 2px rgba(0, 121, 191, 0.1) !important;
        outline: none !important;
    }

    /* Selectbox Styling */
    .stSelectbox > div > div {
        background: white !important;
        border: 1px solid var(--light-grey) !important;
    }

    .stSelectbox > div > div:hover {
        border-color: var(--hover-blue) !important;
    }

    /* Account Cards */
    .account-card {
        background: var(--primary-blue);
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px var(--shadow-medium);
    }

    /* Transaction Rows */
    .transaction-row {
        background: white;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border: 1px solid var(--border-light);
        transition: all 0.2s ease;
    }

    .transaction-row:hover {
        border-color: var(--hover-blue);
        box-shadow: 0 2px 8px var(--shadow-light);
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: #f8f9fa !important;
        border-right: 1px solid var(--border-light) !important;
    }

    .sidebar .sidebar-content {
        background: #f8f9fa;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f8f9fa;
        padding: 0.3rem;
        border-radius: 6px;
        border: 1px solid var(--border-light);
    }

    .stTabs [data-baseweb="tab"] {
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 4px;
        color: var(--text-dark);
        font-weight: 500;
        padding: 0.6rem 1rem;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: #f8f9fa;
        border-color: var(--hover-blue);
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary-blue) !important;
        color: white !important;
        border-color: var(--primary-blue) !important;
    }

    /* Data Table Styling */
    .stDataFrame {
        border: 1px solid var(--border-light);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px var(--shadow-light);
    }

    .stDataFrame table {
        background: white;
    }

    .stDataFrame th {
        background: var(--primary-blue) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.8rem !important;
        border: none !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .stDataFrame td {
        padding: 0.7rem !important;
        border-bottom: 1px solid var(--border-light) !important;
        color: var(--text-dark) !important;
    }

    .stDataFrame tr:hover {
        background: #f8f9fa !important;
    }

    /* Metric Styling */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px var(--shadow-light);
        transition: all 0.2s ease;
    }

    [data-testid="metric-container"]:hover {
        border-color: var(--hover-blue);
        box-shadow: 0 4px 8px var(--shadow-medium);
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--primary-blue) !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }

    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: var(--text-light) !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    /* Alert Styling */
    .stAlert {
        border-radius: 6px;
        border: 1px solid var(--border-light);
        box-shadow: 0 2px 4px var(--shadow-light);
    }

    .stAlert[data-baseweb="notification"] {
        background: #f0f9ff;
        border-color: var(--primary-blue);
        color: var(--primary-blue);
    }

    /* Success/Error Messages */
    .success-message {
        background: #f0f9ff;
        border: 1px solid var(--primary-blue);
        color: var(--primary-blue);
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }

    .error-message {
        background: #fef2f2;
        border: 1px solid #ef4444;
        color: #dc2626;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }

    /* Form Container */
    .stForm {
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px var(--shadow-light);
        margin: 1rem 0;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border: 1px solid var(--border-light);
        border-radius: 6px;
        color: var(--text-dark);
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .streamlit-expanderHeader:hover {
        background: white;
        border-color: var(--hover-blue);
    }

    /* Custom Divider */
    .custom-divider {
        height: 1px;
        background: var(--border-light);
        margin: 2rem 0;
    }

    /* Info Boxes */
    .info-box {
        background: #f0f9ff;
        border: 1px solid var(--primary-blue);
        color: var(--primary-blue);
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }

    .warning-box {
        background: #fffbeb;
        border: 1px solid #f59e0b;
        color: #d97706;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }

    /* Login/Register Form Styling */
    .auth-container {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px var(--shadow-medium);
        border: 1px solid var(--border-light);
    }

    /* Professional Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: var(--text-dark);
    }

    /* Clean text styling */
    p, span, div {
        color: var(--text-dark);
    }

    /* Progress Bar */
    .stProgress .st-bo {
        background: var(--primary-blue);
    }

    /* Professional Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--light-grey);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-blue);
    }

    /* Clean spacing */
    .element-container {
        margin-bottom: 1rem;
    }

    /* Professional footer */
    .footer-container {
        background: #f8f9fa;
        border: 1px solid var(--border-light);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 2rem;
    }

    .footer-container strong {
        color: var(--primary-blue);
        font-weight: 600;
    }

    .footer-container span {
        color: var(--text-light);
        font-weight: 500;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.6rem;
        }
        
        .dashboard-card {
            padding: 1rem;
        }
        
        .user-info {
            padding: 1rem;
        }
    }

    /* Clean focus states */
    *:focus {
        outline: 2px solid var(--hover-blue);
        outline-offset: 2px;
    }

    /* Remove default streamlit styling */
    .stApp > header {
        background: transparent;
    }

    .stApp {
        background: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

class BankingApplication:
    """Main banking application class using OOP principles"""
    
    def __init__(self):
        self.bank_service = BankManagementService()
        self.auth_ui = create_auth_ui(self.bank_service.auth_service)
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'show_register' not in st.session_state:
            st.session_state.show_register = False
    
    def run(self):
        """Main application entry point"""
        # Authentication Check - Safe access to session state
        if not st.session_state.get('logged_in', False):
            if st.session_state.get('show_register', False):
                self.auth_ui.show_register_page()
            else:
                self.auth_ui.show_login_page()
            return
        
        # Main Application
        self._show_main_application()
    
    def _show_main_application(self):
        """Show main application interface"""
        user = st.session_state.get('user')
        user_role = st.session_state.get('user_role')
        
        if not user or not user_role:
            st.error("Session error. Please login again.")
            self.auth_ui.logout()
            return
        
        # Header with user info
        self._show_header(user)
        
        # Sidebar navigation
        page = self._show_sidebar(user_role)
        
        # Route to appropriate page
        self._route_to_page(page, user, user_role)
        
        # Footer
        self._show_footer(user)
    
    def _show_header(self, user):
        """Show application header"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            <div class="main-header">
                <h1>Professional Bank Management System</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="user-info">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">👤</div>
                <strong>{user.name}</strong><br>
                <small>{user.role.title()}</small>
            </div>
            """, unsafe_allow_html=True)
    
    def _show_sidebar(self, user_role: str) -> str:
        """Show sidebar navigation"""
        st.sidebar.title("Navigation")
        
        # Define pages based on user role
        if user_role == "admin":
            pages = ["Dashboard", "Customer Management", "Account Management", "Transactions", "Reports", "User Management", "Profile"]
        elif user_role == "employee":
            pages = ["Dashboard", "Customer Management", "Account Management", "Transactions", "Reports", "Profile"]
        else:  # customer
            pages = ["My Dashboard", "My Accounts", "My Transactions", "Profile"]
        
        page = st.sidebar.selectbox("Select Page", pages)
        
        # Logout button
        if st.sidebar.button("Logout", type="primary"):
            self.auth_ui.logout()
        
        return page
    
    def _route_to_page(self, page: str, user, user_role: str):
        """Route to appropriate page based on selection"""
        if user_role == "customer":
            self._show_customer_pages(page, user)
        else:
            self._show_admin_employee_pages(page, user_role)
    
    def _show_customer_pages(self, page: str, user):
        """Show customer-specific pages"""
        if page == "My Dashboard":
            self._show_customer_dashboard(user)
        elif page == "My Accounts":
            self._show_customer_accounts(user)
        elif page == "My Transactions":
            self._show_customer_transactions(user)
        elif page == "Profile":
            self.auth_ui.show_user_profile()
    
    def _show_customer_dashboard(self, user):
        """Show customer dashboard"""
        st.title("My Banking Dashboard")
        
        # Get customer's accounts
        customer_accounts = []
        if user.customer_id:
            customer_accounts = self.bank_service.get_customer_accounts(user.customer_id)
        
        if customer_accounts:
            # Account summary
            total_balance = sum(acc.balance for acc in customer_accounts)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Accounts", len(customer_accounts))
            
            with col2:
                st.metric("Total Balance", f"${total_balance:,.2f}")
            
            with col3:
                total_transactions = sum(len(acc.transactions) for acc in customer_accounts)
                st.metric("Total Transactions", total_transactions)
            
            # Account cards
            st.subheader("My Accounts")
            for account in customer_accounts:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{account.id}**")
                        st.write(f"Type: {account.account_type.title()}")
                    
                    with col2:
                        st.metric("Balance", f"${account.balance:,.2f}")
                    
                    with col3:
                        st.write(f"Status: {account.status.title()}")
                    
                    with col4:
                        st.metric("Transactions", len(account.transactions))
                    
                    st.divider()
        else:
            st.info("No accounts found. Please contact bank staff to create an account.")
    
    def _show_customer_accounts(self, user):
        """Show customer accounts"""
        st.title("My Accounts")
        
        if user.customer_id:
            customer_accounts = self.bank_service.get_customer_accounts(user.customer_id)
            if customer_accounts:
                for account in customer_accounts:
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h3>Account: {account.id}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Type:** {account.account_type.title()}")
                        st.write(f"**Balance:** ${account.balance:,.2f}")
                        st.write(f"**Status:** {account.status.title()}")
                    
                    with col2:
                        st.write(f"**Created:** {account.created_at[:10]}")
                        st.write(f"**Transactions:** {len(account.transactions)}")
                    
                    # Recent transactions
                    recent_transactions = account.get_transaction_history(limit=5)
                    if recent_transactions:
                        st.write("**Recent Transactions:**")
                        for trans in recent_transactions:
                            st.write(f"- {trans.transaction_type.title()}: ${trans.amount:,.2f} on {trans.created_at[:10]}")
                    
                    st.divider()
            else:
                st.info("No accounts found.")
    
    def _show_customer_transactions(self, user):
        """Show customer transactions"""
        st.title("My Transaction History")
        
        if user.customer_id:
            customer_accounts = self.bank_service.get_customer_accounts(user.customer_id)
            
            if customer_accounts:
                # Account selector
                account_options = {f"{acc.id} (${acc.balance:,.2f})": acc.id for acc in customer_accounts}
                selected_account = st.selectbox("Select Account", list(account_options.keys()))
                
                if selected_account:
                    account_id = account_options[selected_account]
                    account = self.bank_service.get_account(account_id)
                    transactions = account.get_transaction_history(limit=50)
                    
                    if transactions:
                        transaction_data = []
                        for trans in transactions:
                            transaction_data.append({
                                "Date": trans.created_at[:19].replace('T', ' '),
                                "Type": trans.transaction_type.replace('_', ' ').title(),
                                "Amount": f"${trans.amount:,.2f}",
                                "Balance After": f"${trans.balance_after:,.2f}",
                                "Description": trans.description
                            })
                        
                        df = pd.DataFrame(transaction_data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No transactions found for this account.")
            else:
                st.info("No accounts found.")
    
    def _show_admin_employee_pages(self, page: str, user_role: str):
        """Show admin and employee pages"""
        if page == "Dashboard":
            self._show_dashboard()
        elif page == "User Management" and user_role == "admin":
            self._show_user_management()
        elif page == "Customer Management":
            self._show_customer_management()
        elif page == "Account Management":
            self._show_account_management()
        elif page == "Transactions":
            self._show_transactions()
        elif page == "Reports":
            self._show_reports()
        elif page == "Profile":
            self.auth_ui.show_user_profile()
    
    def _show_dashboard(self):
        """Show main dashboard"""
        st.title("Dashboard Overview")
        
        # Get bank summary
        summary = self.bank_service.get_bank_summary()
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Customers", summary['total_customers'])
        
        with col2:
            st.metric("Total Accounts", summary['total_accounts'])
        
        with col3:
            st.metric("Active Accounts", summary['active_accounts'])
        
        with col4:
            st.metric("Total Balance", f"${summary['total_balance']:,.2f}")
        
        # Charts
        if self.bank_service.get_all_accounts():
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Account Types Distribution")
                accounts = self.bank_service.get_all_accounts()
                account_types = {}
                for account in accounts:
                    account_types[account.account_type] = account_types.get(account.account_type, 0) + 1
                
                if account_types:
                    fig = px.pie(
                        values=list(account_types.values()),
                        names=list(account_types.keys()),
                        color_discrete_sequence=['#0079bf', '#329cf7', '#bac5cc', '#7f8c8d']
                    )
                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font_color='#2c3e50'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Account Balances")
                balances = [account.balance for account in accounts]
                account_ids = [account.id for account in accounts]
                
                fig = go.Figure(data=[go.Bar(x=account_ids, y=balances, marker_color='#0079bf')])
                fig.update_layout(
                    title="Account Balances", 
                    xaxis_title="Account ID", 
                    yaxis_title="Balance ($)",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font_color='#2c3e50'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _show_user_management(self):
        """Show user management page"""
        st.title("User Management")
        
        tab1, tab2 = st.tabs(["All Users", "Add User"])
        
        with tab1:
            st.subheader("System Users")
            
            users = self.bank_service.auth_service.get_all_users()
            if users:
                user_data = []
                for u in users:
                    user_data.append({
                        "Username": u.username,
                        "Full Name": u.name,
                        "Email": u.email,
                        "Role": u.role.title(),
                        "Status": "Active" if u.is_active else "Inactive",
                        "Last Login": u.last_login[:19].replace('T', ' ') if u.last_login else "Never",
                        "Created": u.created_at[:10]
                    })
                
                df = pd.DataFrame(user_data)
                st.dataframe(df, use_container_width=True)
                
                # User management actions
                st.subheader("User Actions")
                col1, col2 = st.columns(2)
                
                with col1:
                    user_to_manage = st.selectbox("Select User", [u.username for u in users if u.username != "admin"])
                    
                    if user_to_manage:
                        selected_user = self.bank_service.auth_service.get_user(user_to_manage)
                        current_status = "Active" if selected_user.is_active else "Inactive"
                        st.write(f"Current Status: {current_status}")
                        
                        if st.button("Toggle Status"):
                            new_status = not selected_user.is_active
                            if self.bank_service.auth_service.update_user_status(user_to_manage, new_status):
                                st.success(f"User status updated to {'Active' if new_status else 'Inactive'}")
                                st.rerun()
                
                with col2:
                    if user_to_manage and user_to_manage != "admin":
                        st.write("**Danger Zone**")
                        if st.button("Delete User", type="secondary"):
                            if self.bank_service.auth_service.delete_user(user_to_manage):
                                st.success("User deleted successfully")
                                st.rerun()
            else:
                st.info("No users found.")
        
        with tab2:
            st.subheader("Add New User")
            self.auth_ui.show_register_page()
    
    def _show_customer_management(self):
        """Show customer management page"""
        st.title("Customer Management")
        
        tab1, tab2 = st.tabs(["Add Customer", "View Customers"])
        
        with tab1:
            st.subheader("Add New Customer")
            
            with st.form("add_customer_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Full Name*")
                    email = st.text_input("Email*")
                
                with col2:
                    phone = st.text_input("Phone Number*")
                    address = st.text_area("Address*")
                
                submitted = st.form_submit_button("Add Customer", type="primary")
                
                if submitted:
                    if name and email and phone and address:
                        try:
                            customer = self.bank_service.create_customer(name, email, phone, address)
                            st.success(f"Customer added successfully! Customer ID: {customer.id}")
                        except Exception as e:
                            st.error(f"Error adding customer: {str(e)}")
                    else:
                        st.error("Please fill in all required fields.")
        
        with tab2:
            st.subheader("All Customers")
            
            customers = self.bank_service.get_all_customers()
            if customers:
                # Create DataFrame for display
                customer_data = []
                for customer in customers:
                    accounts = self.bank_service.get_customer_accounts(customer.id)
                    total_balance = sum(acc.balance for acc in accounts)
                    
                    customer_data.append({
                        "Customer ID": customer.id,
                        "Name": customer.name,
                        "Email": customer.email,
                        "Phone": customer.phone,
                        "Accounts": len(accounts),
                        "Total Balance": f"${total_balance:,.2f}",
                        "Created Date": customer.created_at[:10]
                    })
                
                df = pd.DataFrame(customer_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No customers found. Add some customers to get started!")
    
    def _show_account_management(self):
        """Show account management page"""
        st.title("Account Management")
        
        tab1, tab2 = st.tabs(["Create Account", "View Accounts"])
        
        with tab1:
            st.subheader("Create New Account")
            
            customers = self.bank_service.get_all_customers()
            if not customers:
                st.warning("No customers found. Please add customers first.")
            else:
                with st.form("create_account_form"):
                    # Customer selection
                    customer_options = {f"{c.name} ({c.id})": c.id for c in customers}
                    selected_customer = st.selectbox("Select Customer*", list(customer_options.keys()))
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        account_type = st.selectbox("Account Type*", ["savings", "checking", "business"])
                    
                    with col2:
                        initial_deposit = st.number_input("Initial Deposit ($)", min_value=0.0, value=0.0, step=10.0)
                    
                    submitted = st.form_submit_button("Create Account", type="primary")
                    
                    if submitted:
                        try:
                            customer_id = customer_options[selected_customer]
                            account = self.bank_service.create_account(customer_id, account_type, initial_deposit)
                            st.success(f"Account created successfully! Account ID: {account.id}")
                        except Exception as e:
                            st.error(f"Error creating account: {str(e)}")
        
        with tab2:
            st.subheader("All Accounts")
            
            accounts = self.bank_service.get_all_accounts()
            if accounts:
                for account in accounts:
                    customer = self.bank_service.get_customer(account.customer_id)
                    
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3>{account.id}</h3>
                                <p style="margin: 0.5rem 0; color: #7f8c8d;">
                                    Customer: {customer.name if customer else 'Unknown'}<br>
                                    Type: {account.account_type.title()}
                                </p>
                            </div>
                            <div style="text-align: right;">
                                <h2>${account.balance:,.2f}</h2>
                                <p style="margin: 0.5rem 0; color: #7f8c8d;">
                                    Status: {account.status.title()}<br>
                                    Transactions: {len(account.transactions)}
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No accounts found. Create some accounts to get started!")
    
    def _show_transactions(self):
        """Show transactions page"""
        st.title("Transaction Management")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Deposit", "Withdraw", "Transfer", "Transaction History"])
        
        accounts = self.bank_service.get_all_accounts()
        if not accounts:
            st.warning("No accounts found. Please create accounts first.")
        else:
            account_options = {f"{acc.id} (${acc.balance:,.2f})": acc.id for acc in accounts}
            
            with tab1:
                st.subheader("Make Deposit")
                
                with st.form("deposit_form"):
                    selected_account = st.selectbox("Select Account", list(account_options.keys()))
                    amount = st.number_input("Deposit Amount ($)", min_value=0.01, step=10.0)
                    description = st.text_input("Description (Optional)", value="Deposit")
                    
                    submitted = st.form_submit_button("Make Deposit", type="primary")
                    
                    if submitted:
                        try:
                            account_id = account_options[selected_account]
                            account = self.bank_service.get_account(account_id)
                            transaction = account.deposit(amount, description)
                            self.bank_service._save_data()
                            st.success(f"Deposit successful! New balance: ${account.balance:,.2f}")
                        except Exception as e:
                            st.error(f"Error making deposit: {str(e)}")
            
            with tab2:
                st.subheader("Make Withdrawal")
                
                with st.form("withdraw_form"):
                    selected_account = st.selectbox("Select Account", list(account_options.keys()), key="withdraw_account")
                    amount = st.number_input("Withdrawal Amount ($)", min_value=0.01, step=10.0, key="withdraw_amount")
                    description = st.text_input("Description (Optional)", value="Withdrawal", key="withdraw_desc")
                    
                    submitted = st.form_submit_button("Make Withdrawal", type="primary")
                    
                    if submitted:
                        try:
                            account_id = account_options[selected_account]
                            account = self.bank_service.get_account(account_id)
                            transaction = account.withdraw(amount, description)
                            self.bank_service._save_data()
                            st.success(f"Withdrawal successful! New balance: ${account.balance:,.2f}")
                        except Exception as e:
                            st.error(f"Error making withdrawal: {str(e)}")
            
            with tab3:
                st.subheader("Transfer Funds")
                
                with st.form("transfer_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        from_account = st.selectbox("From Account", list(account_options.keys()), key="from_account")
                    
                    with col2:
                        to_account = st.selectbox("To Account", list(account_options.keys()), key="to_account")
                    
                    amount = st.number_input("Transfer Amount ($)", min_value=0.01, step=10.0, key="transfer_amount")
                    description = st.text_input("Description (Optional)", value="Transfer", key="transfer_desc")
                    
                    submitted = st.form_submit_button("Transfer Funds", type="primary")
                    
                    if submitted:
                        try:
                            from_account_id = account_options[from_account]
                            to_account_id = account_options[to_account]
                            
                            if from_account_id == to_account_id:
                                st.error("Cannot transfer to the same account!")
                            else:
                                from_trans, to_trans = self.bank_service.transfer_funds(from_account_id, to_account_id, amount, description)
                                st.success(f"Transfer successful! Amount: ${amount:,.2f}")
                        except Exception as e:
                            st.error(f"Error making transfer: {str(e)}")
            
            with tab4:
                st.subheader("Transaction History")
                
                selected_account = st.selectbox("Select Account for History", list(account_options.keys()), key="history_account")
                
                if selected_account:
                    account_id = account_options[selected_account]
                    account = self.bank_service.get_account(account_id)
                    transactions = account.get_transaction_history(limit=50)
                    
                    if transactions:
                        transaction_data = []
                        for trans in transactions:
                            transaction_data.append({
                                "Date": trans.created_at[:19].replace('T', ' '),
                                "Type": trans.transaction_type.replace('_', ' ').title(),
                                "Amount": f"${trans.amount:,.2f}",
                                "Balance After": f"${trans.balance_after:,.2f}",
                                "Description": trans.description,
                                "Reference": trans.reference_account or "-"
                            })
                        
                        df = pd.DataFrame(transaction_data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No transactions found for this account.")
    
    def _show_reports(self):
        """Show reports page"""
        st.title("Reports & Analytics")
        
        accounts = self.bank_service.get_all_accounts()
        customers = self.bank_service.get_all_customers()
        
        if not accounts:
            st.warning("No data available for reports.")
        else:
            tab1, tab2, tab3 = st.tabs(["Summary Report", "Customer Report", "Transaction Report"])
            
            with tab1:
                st.subheader("Bank Summary Report")
                
                summary = self.bank_service.get_bank_summary()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Total Customers", summary['total_customers'])
                    st.metric("Total Accounts", summary['total_accounts'])
                    st.metric("Active Accounts", summary['active_accounts'])
                    st.metric("Total Bank Balance", f"${summary['total_balance']:,.2f}")
                
                with col2:
                    # Account type distribution
                    account_types = {}
                    for account in accounts:
                        account_types[account.account_type] = account_types.get(account.account_type, 0) + 1
                    
                    st.write("**Account Types:**")
                    for acc_type, count in account_types.items():
                        st.write(f"- {acc_type.title()}: {count}")
            
            with tab2:
                st.subheader("Customer Report")
                
                customer_data = []
                for customer in customers:
                    customer_accounts = self.bank_service.get_customer_accounts(customer.id)
                    total_balance = sum(acc.balance for acc in customer_accounts)
                    total_transactions = sum(len(acc.transactions) for acc in customer_accounts)
                    
                    customer_data.append({
                        "Customer ID": customer.id,
                        "Name": customer.name,
                        "Email": customer.email,
                        "Phone": customer.phone,
                        "Accounts": len(customer_accounts),
                        "Total Balance": total_balance,
                        "Total Transactions": total_transactions,
                        "Member Since": customer.created_at[:10]
                    })
                
                if customer_data:
                    df = pd.DataFrame(customer_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Top customers by balance
                    st.subheader("Top Customers by Balance")
                    top_customers = df.nlargest(5, 'Total Balance')
                    fig = px.bar(
                        top_customers,
                        x='Name',
                        y='Total Balance',
                        title="Top 5 Customers by Balance",
                        color_discrete_sequence=['#0079bf']
                    )
                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font_color='#2c3e50'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("Transaction Report")
                
                all_transactions = []
                for account in accounts:
                    for trans in account.transactions:
                        customer = self.bank_service.get_customer(account.customer_id)
                        all_transactions.append({
                            "Date": trans.created_at[:10],
                            "Account ID": trans.account_id,
                            "Customer": customer.name if customer else "Unknown",
                            "Type": trans.transaction_type.replace('_', ' ').title(),
                            "Amount": trans.amount,
                            "Description": trans.description
                        })
                
                if all_transactions:
                    df = pd.DataFrame(all_transactions)
                    
                    # Recent transactions
                    st.write("**Recent Transactions (Last 20):**")
                    recent_df = df.head(20)
                    st.dataframe(recent_df, use_container_width=True)
                    
                    # Transaction type distribution
                    st.subheader("Transaction Types Distribution")
                    type_counts = df['Type'].value_counts()
                    fig = px.pie(
                        values=type_counts.values,
                        names=type_counts.index,
                        title="Transaction Types",
                        color_discrete_sequence=['#0079bf', '#329cf7', '#bac5cc', '#7f8c8d']
                    )
                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font_color='#2c3e50'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No transactions found.")
    
    def _show_footer(self, user):
        """Show application footer"""
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""<div class="footer-container">
                <strong>Professional Bank Management System</strong><br>
                <span>Logged in as: {user.name} ({user.role.title()})</span>
            </div>""",
            unsafe_allow_html=True
        )

# Initialize and run the application
@st.cache_resource
def get_application():
    """Get cached application instance"""
    return BankingApplication()

# Main execution
if __name__ == "__main__":
    app = get_application()
    app.run()
