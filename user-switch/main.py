import yaml
from simple_term_menu import TerminalMenu
from colored import Fore, Back, Style

config_file = 'console.yaml'

class Users:
    def __init__(self, filename):
        self.load_users(filename)

    def load_users(self, filename):
        """Loads users from console.yaml"""
        try:
            with open(filename, 'r') as file:
                dict = yaml.safe_load(file)['Users']
                self.data = [dict[user] for user in dict]
        except FileNotFoundError:
            error("console.yaml not found in current directory")

    def get_names(self):
        return [user['Name'] for user in self.data]

    def get_by_index(self, index):
        return self.data[index]


def error(message: str):
    print(f'{Fore.red}{message}')
    exit()

def update_env(user: dict):
    """Updates .env.local with selected user's credentials"""
    with open('.env.local', 'w') as file:
        file.write(f"VITE_DHIS_AUTH={user['Auth']}\n")

    print(f"User {Fore.green}{user['Name']}{Style.reset} ({user['Username']}) selected.\n")


users = Users(config_file)
menu = TerminalMenu(users.get_names())
selected_user = users.get_by_index(menu.show())
update_env(selected_user)


