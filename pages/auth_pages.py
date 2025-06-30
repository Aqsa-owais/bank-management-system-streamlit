import streamlit as st
from scripts.services import UserAuthService

class AuthenticationUI:
    """Authentication UI class using OOP principles"""
    
    def __init__(self, auth_service: UserAuthService):
        self.auth_service = auth_service
    
    def show_login_page(self):
        """Display login page"""
        st.markdown("""
        <div style="max-width: 450px; margin: 0 auto; padding: 2rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: #0079bf; font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;">
                     Bank Login
                </h1>
                <p style="color: #7f8c8d; font-size: 1.1rem;">Please login to access the banking system</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Center the login form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Create a styled container
            st.markdown("""
            <div class="auth-container">
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.markdown("### Login to Your Account")
                
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col_login, col_register = st.columns(2)
                
                with col_login:
                    login_clicked = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                with col_register:
                    register_clicked = st.form_submit_button("Register", use_container_width=True)
                
                if login_clicked:
                    self._handle_login(username, password)
                
                if register_clicked:
                    st.session_state.show_register = True
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Default credentials info
            self._show_default_credentials()
    
    def _handle_login(self, username: str, password: str):
        """Handle login logic"""
        if username and password:
            success, message, user = self.auth_service.login(username, password)
            
            if success:
                # Store user info in session state
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.username = user.username
                st.session_state.user_role = user.role
                st.session_state.user_id = user.id
                
                st.success(f"Welcome back, {user.name}!")
                st.rerun()
            else:
                st.error(f"❌ {message}")
        else:
            st.error("Please enter both username and password")
    
    def _show_default_credentials(self):
        """Show default credentials info"""
        with st.expander("Default Login Credentials", expanded=False):
            st.markdown("""
            <div class="info-box">
                <strong> Default Admin Account:</strong><br>
                • Username: <code>admin</code><br>
                • Password: <code>admin123</code><br>
                • Role: Administrator<br><br>
                <strong> Note:</strong> Please change the default password after first login.
            </div>
            """, unsafe_allow_html=True)
    
    def show_register_page(self):
        """Display registration page"""
        st.markdown("""
        <div style="max-width: 700px; margin: 0 auto; padding: 2rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: #0079bf; font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;">
                     Bank Registration
                </h1>
                <p style="color: #7f8c8d; font-size: 1.1rem;">Create your account to access banking services</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Create a styled container
            st.markdown("""
            <div class="auth-container">
            """, unsafe_allow_html=True)
            
            with st.form("register_form"):
                st.markdown("### Create New Account")
                
                # Basic Information
                col_left, col_right = st.columns(2)
                
                with col_left:
                    full_name = st.text_input("Full Name*", placeholder="Enter your full name")
                    username = st.text_input("Username*", placeholder="Choose a username")
                    email = st.text_input("Email*", placeholder="Enter your email")
                
                with col_right:
                    phone = st.text_input("Phone Number*", placeholder="Enter phone number")
                    password = st.text_input("Password*", type="password", placeholder="Create password (min 6 chars)")
                    confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
                
                # Role selection (for admin registration)
                if st.session_state.get('user_role') == 'admin':
                    role = st.selectbox("User Role", ["customer", "employee", "admin"])
                else:
                    role = "customer"  # Default role for public registration
                
                col_register, col_back = st.columns(2)
                
                with col_register:
                    register_clicked = st.form_submit_button("Register", type="primary", use_container_width=True)
                
                with col_back:
                    back_clicked = st.form_submit_button("Back to Login", use_container_width=True)
                
                if register_clicked:
                    self._handle_registration(full_name, username, email, phone, password, confirm_password, role)
                
                if back_clicked:
                    st.session_state.show_register = False
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    def _handle_registration(self, full_name: str, username: str, email: str, 
                           phone: str, password: str, confirm_password: str, role: str):
        """Handle registration logic"""
        # Validation
        if not all([full_name, username, email, phone, password, confirm_password]):
            st.error("Please fill in all required fields")
        elif password != confirm_password:
            st.error("❌ Passwords do not match")
        elif len(password) < 6:
            st.error("🔒 Password must be at least 6 characters long")
        else:
            success, message, user = self.auth_service.register_user(
                username=username,
                email=email,
                password=password,
                role=role,
                full_name=full_name,
                phone=phone
            )
            
            if success:
                st.success("Registration successful! You can now login.")
                st.balloons()
                
                # Auto login for customer registration
                if role == "customer":
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.username = user.username
                    st.session_state.user_role = user.role
                    st.session_state.user_id = user.id
                    st.rerun()
                else:
                    st.session_state.show_register = False
                    st.rerun()
            else:
                st.error(f"❌ {message}")
    
    def show_user_profile(self):
        """Display user profile page"""
        if 'user' not in st.session_state:
            return
        
        user = st.session_state.user
        
        st.title("User Profile")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div style="background: #0079bf; color: white; padding: 2rem; border-radius: 8px; 
                        text-align: center; box-shadow: 0 4px 12px rgba(0, 121, 191, 0.15);">
                <h2 style="margin: 0; color: white; font-size: 3rem;"></h2>
                <h3 style="margin: 0.5rem 0; color: white;">{user.name}</h3>
                <p style="margin: 0; opacity: 0.9;">@{user.username}</p>
                <p style="margin: 0.5rem 0; opacity: 0.9; background: rgba(255,255,255,0.2); 
                   padding: 0.5rem; border-radius: 12px;">{user.role.title()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Account Information")
            
            # Create styled info cards
            info_data = {
                "User ID": user.id,
                "Username": user.username,
                "Full Name": user.name,
                "Email": user.email,
                "Phone": user.phone,
                "Role": user.role.title(),
                "Status": "Active" if user.is_active else "Inactive",
                "Member Since": user.created_at[:10],
                "Last Login": user.last_login[:19].replace('T', ' ') if user.last_login else "Never"
            }
            
            for key, value in info_data.items():
                st.markdown(f"""
                <div style="background: white; padding: 0.8rem; margin: 0.5rem 0; border-radius: 6px;
                            border: 1px solid #e8ecef; box-shadow: 0 2px 4px rgba(0, 121, 191, 0.05);">
                    <strong style="color: #0079bf;">{key}:</strong> 
                    <span style="color: #2c3e50;">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Change Password Section
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.subheader("Change Password")
        
        with st.form("change_password_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
            
            with col2:
                confirm_new_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password", type="primary"):
                self._handle_password_change(user, current_password, new_password, confirm_new_password)
    
    def _handle_password_change(self, user, current_password: str, new_password: str, confirm_new_password: str):
        """Handle password change logic"""
        if not all([current_password, new_password, confirm_new_password]):
            st.error("Please fill in all password fields")
        elif not user.check_password(current_password):
            st.error("Current password is incorrect")
        elif new_password != confirm_new_password:
            st.error("New passwords do not match")
        elif len(new_password) < 6:
            st.error("New password must be at least 6 characters long")
        else:
            # Update password
            user.change_password(new_password)
            self.auth_service._users[user.username] = user
            self.auth_service._save_users()
            st.success("Password changed successfully!")
    
    @staticmethod
    def logout():
        """Logout user and clear session"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Factory function to create authentication UI
def create_auth_ui(auth_service: UserAuthService) -> AuthenticationUI:
    """Factory function to create authentication UI"""
    return AuthenticationUI(auth_service)
