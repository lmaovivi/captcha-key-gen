import random
import requests
import string
import threading
import colorama
import time

class GenerateCapSolverKey():
    def __init__(self):
        self.threads = 0
        self.workingKeys = []
        self.amount = 5
        self.proxies = []

    def _print(self, message, color=colorama.Fore.BLUE):
        print("[+] " + color + message + colorama.Style.RESET_ALL)

    def loadProxies(self):
        try:
            with open('config/proxies.txt', 'r') as file:
                self.proxies = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self._print('Proxies file not found. Running without proxies.')

    def generateKey(self, amount):
        letters = string.ascii_uppercase + string.digits
        keys = []
        for i in range(amount):
            key = "CAP-" + ''.join(random.choice(letters) for i in range(32))
            keys.append(key)

        return keys

    def checkKey(self, key):
        try:
            proxy = random.choice(self.proxies) if self.proxies else None
            response = requests.post('https://api.capsolver.com/getBalance', json={'clientKey': key}, proxies=proxy).json()
            if response['errorid'] == 0:
                self._print(f"Valid Key found! : {key}", colorama.Fore.GREEN)
                self._print(f"Key balance: " +  response['balance'])
                self.workingKeys.append(key)
        except Exception as e:
            pass

def capsolver():
    colorama.init(autoreset=True)
    generator = GenerateCapSolverKey()
    
    generator._print('--- CapSolver Key Gen ---', colorama.Fore.CYAN)
    generator.threads = int(input('Enter the number of threads: '))
    generator.amount = int(input('Enter the number of keys to generate: '))
    generator.loadProxies()
    
    generator._print('Starting the Captcha Key Gen, please wait!')
    time.sleep(2)
    
    threads = []
    keys = generator.generateKey(generator.amount * generator.threads)

    for key in keys:
        thread = threading.Thread(target=generator.checkKey, args=(key,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    generator._print(f'Found {len(generator.workingKeys)} valid keys', colorama.Fore.YELLOW)
    for valid_key in generator.workingKeys:
        generator._print(valid_key, colorama.Fore.GREEN)
