#!/usr/bin/env python3

import requests
import threading
import sys
import random

# List of User-Agent strings for spoofing requests
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

# Function to attempt to discover directories
def sneak_in(ip, dir_name):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        res = requests.get(f'http://{ip}/{dir_name}', headers=headers)
        if res.status_code == 200:  # Only show useful results
            print(f'[✅] Found: http://{ip}/{dir_name} -> 200 (OK)')
        elif res.status_code in [301, 302]:  # Redirects can be useful too
            print(f'[↪️] Redirect: http://{ip}/{dir_name} -> {res.status_code} (Redirect)')
    except Exception as e:
        print(f'[❌] ERROR: {str(e)}')

# Main function to handle user input and start threading
def main():
    ip = input('🖥️  Enter Target IP: ')
    file = input('📂 Enter Wordlist File Path: ')
    print('\n' + '=' * 50)
    print('🚀  Starting Directory Discovery  🚀')
    print('=' * 50 + '\n')

    threads = []
    with open(file, 'r') as p_file:
        p_file = p_file.readlines()
        sneaked = []
        for dir_name in p_file:
            try:
                if dir_name not in sneaked:
                    sneaked.append(dir_name)
                    dir_name = dir_name.strip()
                    th = threading.Thread(target=sneak_in, args=(ip, dir_name))
                    threads.append(th)
                    th.start()
            except KeyboardInterrupt:
                print('\n[-] Terminating...')
                sys.exit()

        for thread in threads:
            thread.join()

    print('\n' + '=' * 50)
    print('🎉  Discovery Complete!  🎉')
    print('=' * 50 + '\n')

if __name__ == '__main__':
    main()
