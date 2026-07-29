import json


class UserFactory:
    def __init__(self, domain):
        self.domain = domain[1:] if domain.startswith('@') else domain
        self.user_list = []
        self.role_permissions = {
            "Admin": ["create", "edit", "delete", "view"],
            "Editor": ["edit", "view"],
            "Viewer": ["view"],
        }

    def _calculate_status(self, age):
        if not isinstance(age, int) or age <= 0:
            print("Couldn't change age. Invalid Age.\n")
        else:
            return 'Minor' if age < 18 else 'Senior' if age > 65 else 'Adult'

    def create_user(self, name, age, role='Viewer'):

        email = f'{name}@{self.domain}'.lower()
        for user in self.user_list:
            if email == user['email']:
                print(f'ERROR. User {name} with "{email}" email already exists.\n')
                return
        status = self._calculate_status(age)
        user = {
            'name': name,
            'email': email,
            'age': age,
            'status': status,
            'role': role,
        }
        self.user_list.append(user)
        print(f'User {name} created successfully.\n')

    def _get_user(self, email):
        lowered_email = email.lower()
        for user in self.user_list:
            if user['email'] == lowered_email:
                return user

    def display_all_users(self):
        formatted_users = json.dumps(self.user_list, indent=4)
        return formatted_users

    def get_stats(self):
        status_dict = {
            'Minor': 0,
            'Adult': 0,
            'Senior': 0,
        }
        for user in self.user_list:
            if user['status'] == 'Minor':
                status_dict['Minor'] += 1
            elif user['status'] == 'Adult':
                status_dict['Adult'] += 1
            elif user['status'] == 'Senior':
                status_dict['Senior'] += 1
            else:
                print(f"Warning: Unknown status found: {user['status']}")

        print(f'\n{status_dict}\n')

    def delete_user_by_email(self, email):
        user = self._get_user(email)
        try:
            self.user_list.remove(user)
            print(f'User {email} deleted.\n')
            return
        except:
            print(f"ERROR: User '{email}' not found.\n")

    def update_user_info(self, email, **kwargs):
        user = self._get_user(email)
        if not user:
            return f"Error: User '{email}' not found.\n"
        for key, value in kwargs.items():
            user[key] = value
            if key == 'age':
                user['status'] = self._calculate_status(value)

        print(f"User {email} updated successfully.\n")

    def get_user_permissions(self, email):
        user = self._get_user(email)
        if not user:
            return f"ERROR: User '{email}' not found."
        if user['role'] in self.role_permissions:
            user_permissions = self.role_permissions.get(user['role'], [])
            return f"Permissions for user '{email}': {user_permissions}\n"


domain = UserFactory('@google.com')
domain.create_user('David', 60)
domain.create_user('Mike', 15)
domain.create_user('Sasha', 18)
domain.create_user('mike', 15)
domain.create_user('Clair', 66)
domain.create_user('Batholomew', 76)
domain.update_user_info('clair@google.com', age=10, role='Admin')
domain.delete_user_by_email('sasha@google.com')
domain.delete_user_by_email('sasa@google.com')
domain.create_user('Morah', 53, 'Admin')
domain.create_user('Chris', 26, 'Editor')
print(domain.display_all_users())
domain.get_stats()
print(domain.get_user_permissions('chris@google.com'))
print(domain.get_user_permissions('chris@oogle.com'))
