#!/usr/bin/env python3

import socket
import threading
from colorama import Fore, Style, init

# Initialize Colorama
init()

# Function to scan a specific port
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            print(Fore.GREEN + f'[✅] Port {port} is open.' + Style.RESET_ALL)
        sock.close()
    except Exception as e:
        print(Fore.YELLOW + f'[⚠️] Error scanning port {port}: {str(e)}' + Style.RESET_ALL)

# Main function to get user input and start scanning
def main():
    ip = input('🖥️  Enter an IP address to scan: ')
    print(Fore.CYAN + f'[+] Scanning {ip} for open ports (1-1000)...' + Style.RESET_ALL)
    ports = range(1, 1001)
    threads = []
    
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(Fore.MAGENTA + '[🎉] Scanning completed!' + Style.RESET_ALL)

if __name__ == '__main__':
    main()
