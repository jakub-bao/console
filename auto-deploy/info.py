from colored import Fore, Back, Style


def info(message):
    print(f'{message}')


def error(message: str):
    print(f'{Fore.red}{message}')
    exit()