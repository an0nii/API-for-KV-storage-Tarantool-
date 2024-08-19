from auth import create_user
import os

def create_admin_user():
    admin_username = os.environ.get('ADMIN_LOGIN', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'presale')
    if create_user(admin_username, admin_password):
        print(f"Admin user '{admin_username}' created successfully.")
    else:
        print(f"Admin user '{admin_username}' already exists.")

create_admin_user()