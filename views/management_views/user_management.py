import tkinter as tk
from tkinter import ttk, messagebox
from config import Config
from assets.styles.theme import theme
from controllers.user_controller import UserController
from utils.validators import Validators
from utils.constants import UserRoles

class UserManagementView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.user_controller = UserController()
        self.selected_user_id = None
        
        self.setup_ui()
        self.load_users()
    
    def setup_ui(self):
        # Main container
        container = ttk.Frame(self.parent, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="User Management", 
                 style='Title.TLabel', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Two-column layout
        main_frame = ttk.Frame(container, style='Modern.TFrame')
        main_frame.pack(fill='both', expand=True)
        
        # Left side - User List
        left_frame = ttk.Frame(main_frame, style='Modern.TFrame', width=400)
        left_frame.pack(side='left', fill='both', padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Right side - User Form
        right_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # User List Card
        list_card = theme.create_card(left_frame)
        list_card.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(list_card, text="Users List", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        # Search box
        search_frame = ttk.Frame(list_card, style='Modern.TFrame')
        search_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:", style='Normal.TLabel').pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                style='Modern.TEntry', width=20)
        search_entry.pack(side='left', padx=(10, 5))
        search_entry.bind('<KeyRelease>', self.filter_users)
        
        # Users Table
        columns = ('username', 'full_name', 'role', 'status')
        self.users_tree = ttk.Treeview(list_card, columns=columns, show='headings', style='Modern.Treeview', height=15)
        
        self.users_tree.heading('username', text='Username')
        self.users_tree.heading('full_name', text='Full Name')
        self.users_tree.heading('role', text='Role')
        self.users_tree.heading('status', text='Status')
        
        self.users_tree.column('username', width=100)
        self.users_tree.column('full_name', width=150)
        self.users_tree.column('role', width=80)
        self.users_tree.column('status', width=80)
        
        scrollbar = ttk.Scrollbar(list_card, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side='left', fill='both', expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side='right', fill='y', padx=(0, 15), pady=(0, 15))
        
        # Bind selection
        self.users_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        
        # User Form Card
        form_card = theme.create_card(right_frame)
        form_card.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(form_card, text="User Details", style='Heading.TLabel').pack(anchor='w', padx=15, pady=15)
        
        # Form content
        form_content = ttk.Frame(form_card, style='Modern.TFrame')
        form_content.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Username
        ttk.Label(form_content, text="Username *", style='Normal.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(form_content, textvariable=self.username_var,
                                       style='Modern.TEntry', width=25)
        self.username_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Full Name
        ttk.Label(form_content, text="Full Name *", style='Normal.TLabel').grid(row=0, column=2, sticky='w', pady=8)
        self.full_name_var = tk.StringVar()
        self.full_name_entry = ttk.Entry(form_content, textvariable=self.full_name_var,
                                        style='Modern.TEntry', width=25)
        self.full_name_entry.grid(row=0, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # Password
        ttk.Label(form_content, text="Password", style='Normal.TLabel').grid(row=1, column=0, sticky='w', pady=8)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(form_content, textvariable=self.password_var,
                                       style='Modern.TEntry', width=25, show="•")
        self.password_entry.grid(row=1, column=1, sticky='w', pady=8, padx=(10, 20))
        ttk.Label(form_content, text="(Leave blank to keep current)", style='Small.TLabel',
                 foreground=Config.THEME['text_secondary']).grid(row=1, column=2, sticky='w', pady=8)
        
        # Email
        ttk.Label(form_content, text="Email", style='Normal.TLabel').grid(row=2, column=0, sticky='w', pady=8)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_content, textvariable=self.email_var,
                                    style='Modern.TEntry', width=25)
        self.email_entry.grid(row=2, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Phone
        ttk.Label(form_content, text="Phone", style='Normal.TLabel').grid(row=2, column=2, sticky='w', pady=8)
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(form_content, textvariable=self.phone_var,
                                    style='Modern.TEntry', width=25)
        self.phone_entry.grid(row=2, column=3, sticky='w', pady=8, padx=(10, 0))
        
        # Role
        ttk.Label(form_content, text="Role *", style='Normal.TLabel').grid(row=3, column=0, sticky='w', pady=8)
        self.role_var = tk.StringVar(value=UserRoles.USER)
        role_combo = ttk.Combobox(form_content, textvariable=self.role_var,
                                 values=[UserRoles.ADMIN, UserRoles.USER, UserRoles.MANAGER],
                                 style='Modern.TCombobox', width=23)
        role_combo.grid(row=3, column=1, sticky='w', pady=8, padx=(10, 20))
        
        # Status
        ttk.Label(form_content, text="Status", style='Normal.TLabel').grid(row=3, column=2, sticky='w', pady=8)
        self.status_var = tk.BooleanVar(value=True)
        status_frame = ttk.Frame(form_content, style='Modern.TFrame')
        status_frame.grid(row=3, column=3, sticky='w', pady=8, padx=(10, 0))
        
        ttk.Radiobutton(status_frame, text="Active", variable=self.status_var,
                       value=True, style='TRadiobutton').pack(side='left', padx=(0, 10))
        ttk.Radiobutton(status_frame, text="Inactive", variable=self.status_var,
                       value=False, style='TRadiobutton').pack(side='left')
        
        # Action Buttons
        action_frame = ttk.Frame(form_content, style='Modern.TFrame')
        action_frame.grid(row=4, column=0, columnspan=4, sticky='w', pady=20)
        
        self.add_btn = ttk.Button(action_frame, text="Add New User", style='Success.TButton',
                                command=self.add_user)
        self.add_btn.pack(side='left', padx=(0, 10))
        
        self.update_btn = ttk.Button(action_frame, text="Update User", style='Modern.TButton',
                                   command=self.update_user, state='disabled')
        self.update_btn.pack(side='left', padx=(0, 10))
        
        self.delete_btn = ttk.Button(action_frame, text="Delete User", style='Danger.TButton',
                                   command=self.delete_user, state='disabled')
        self.delete_btn.pack(side='left', padx=(0, 10))
        
        self.clear_btn = ttk.Button(action_frame, text="Clear Form", style='Secondary.TButton',
                                  command=self.clear_form)
        self.clear_btn.pack(side='left')
        
        # Status message
        self.status_var_msg = tk.StringVar()
        status_label = ttk.Label(form_content, textvariable=self.status_var_msg, style='Normal.TLabel')
        status_label.grid(row=5, column=0, columnspan=4, sticky='w', pady=5)
    
    def load_users(self):
        """Load all users into the treeview"""
        try:
            # Clear existing data
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            users = self.user_controller.get_all_users()
            
            for user in users:
                status = "Active" if user.is_active else "Inactive"
                self.users_tree.insert('', 'end', values=(
                    user.username,
                    user.full_name,
                    user.role,
                    status
                ), tags=(user.id,))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")
    
    def filter_users(self, event=None):
        """Filter users based on search text"""
        search_text = self.search_var.get().lower()
        
        for item in self.users_tree.get_children():
            values = self.users_tree.item(item)['values']
            if (search_text in values[0].lower() or  # username
                search_text in values[1].lower() or  # full_name
                search_text in values[2].lower() or  # role
                search_text in values[3].lower()):   # status
                self.users_tree.item(item, tags=())
            else:
                self.users_tree.item(item, tags=('hidden',))
        
        self.users_tree.tag_configure('hidden', foreground=Config.THEME['text_secondary'])
    
    def on_user_select(self, event):
        """Handle user selection from treeview"""
        selected_items = self.users_tree.selection()
        if not selected_items:
            return
        
        item = selected_items[0]
        values = self.users_tree.item(item)['values']
        user_id = self.users_tree.item(item)['tags'][0]
        
        self.selected_user_id = user_id
        
        # Get user details
        users = self.user_controller.get_all_users()
        user = next((u for u in users if u.id == user_id), None)
        
        if user:
            self.username_var.set(user.username)
            self.full_name_var.set(user.full_name)
            self.email_var.set(user.email or "")
            self.phone_var.set(user.phone or "")
            self.role_var.set(user.role)
            self.status_var.set(user.is_active)
            self.password_var.set("")  # Clear password field
            
            # Enable update and delete buttons
            self.update_btn.configure(state='normal')
            self.delete_btn.configure(state='normal')
            self.add_btn.configure(state='disabled')
            
            self.status_var_msg.set(f"Editing user: {user.username}")
    
    def clear_form(self):
        """Clear the form and reset to add mode"""
        self.username_var.set("")
        self.full_name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.password_var.set("")
        self.role_var.set(UserRoles.USER)
        self.status_var.set(True)
        
        self.selected_user_id = None
        self.users_tree.selection_remove(self.users_tree.selection())
        
        # Enable add button, disable update/delete
        self.add_btn.configure(state='normal')
        self.update_btn.configure(state='disabled')
        self.delete_btn.configure(state='disabled')
        
        self.status_var_msg.set("Ready to add new user")
        self.username_entry.focus()
    
    def validate_form(self, is_new_user=True):
        """Validate form data"""
        username = self.username_var.get().strip()
        full_name = self.full_name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        password = self.password_var.get().strip()
        
        # Required fields
        if not username:
            messagebox.showerror("Error", "Username is required")
            return False
        
        if not full_name:
            messagebox.showerror("Error", "Full name is required")
            return False
        
        # Validate username format
        if not Validators.validate_username(username):
            messagebox.showerror("Error", "Username must be 3-20 characters and contain only letters, numbers, and underscores")
            return False
        
        # Password required for new users
        if is_new_user and not password:
            messagebox.showerror("Error", "Password is required for new users")
            return False
        
        # Validate email if provided
        if email and not Validators.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return False
        
        # Validate phone if provided
        if phone and not Validators.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format (10 digits required)")
            return False
        
        return True
    
    def add_user(self):
        """Add new user"""
        if not self.validate_form(is_new_user=True):
            return
        
        try:
            user_data = {
                'username': self.username_var.get().strip(),
                'password': self.password_var.get().strip(),
                'full_name': self.full_name_var.get().strip(),
                'email': self.email_var.get().strip(),
                'phone': self.phone_var.get().strip(),
                'role': self.role_var.get(),
                'is_active': self.status_var.get()
            }
            
            user_id = self.user_controller.create_user(user_data)
            
            if user_id:
                messagebox.showinfo("Success", f"User '{user_data['username']}' created successfully!")
                self.load_users()
                self.clear_form()
                self.status_var_msg.set("User added successfully")
            else:
                messagebox.showerror("Error", "Failed to create user. Username might already exist.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {str(e)}")
    
    def update_user(self):
        """Update selected user"""
        if not self.selected_user_id:
            messagebox.showerror("Error", "No user selected")
            return
        
        if not self.validate_form(is_new_user=False):
            return
        
        try:
            user_data = {
                'username': self.username_var.get().strip(),
                'full_name': self.full_name_var.get().strip(),
                'email': self.email_var.get().strip(),
                'phone': self.phone_var.get().strip(),
                'role': self.role_var.get(),
                'is_active': self.status_var.get()
            }
            
            # If password is provided, update it
            password = self.password_var.get().strip()
            if password:
                user_data['password'] = password
            
            success = self.user_controller.update_user(self.selected_user_id, user_data)
            
            if success:
                messagebox.showinfo("Success", f"User '{user_data['username']}' updated successfully!")
                self.load_users()
                self.clear_form()
                self.status_var_msg.set("User updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update user")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")
    
    def delete_user(self):
        """Delete selected user"""
        if not self.selected_user_id:
            messagebox.showerror("Error", "No user selected")
            return
        
        # Get user details for confirmation
        users = self.user_controller.get_all_users()
        user = next((u for u in users if u.id == self.selected_user_id), None)
        
        if not user:
            messagebox.showerror("Error", "User not found")
            return
        
        # Prevent self-deletion
        if user.id == self.user.id:
            messagebox.showerror("Error", "You cannot delete your own account")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                             f"Are you sure you want to delete user '{user.username}'?\nThis action cannot be undone."):
            try:
                # In a real implementation, you would call a delete method
                # For now, we'll deactivate the user
                user_data = {
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email or "",
                    'phone': user.phone or "",
                    'role': user.role,
                    'is_active': False
                }
                
                success = self.user_controller.update_user(self.selected_user_id, user_data)
                
                if success:
                    messagebox.showinfo("Success", f"User '{user.username}' has been deactivated")
                    self.load_users()
                    self.clear_form()
                    self.status_var_msg.set("User deactivated")
                else:
                    messagebox.showerror("Error", "Failed to deactivate user")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")