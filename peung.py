#!/usr/bin/python3

import os
import sys
import time
import platform

# FRAME = '-|++++'
FRAME = '─│┌┐└┘'

COLOR = {
    FRAME: '\033[90m',
    '1234567890.': '\033[92m'
}

# Clear command
_clear = 'cls' if platform.system() == 'Windows' else 'clear'
cls = lambda: os.system(_clear)

def ping(addr: str = '8.8.8.8') -> None:
    '''Performs a ping.'''
    
    # Parse
    raw = os.popen(f'ping {addr} -c 1').read().rstrip().split('\n')[-1]
    stats = raw.split()[3].split('/')
    
    # Return
    keys = ['min', 'avg', 'max', 'mdev']
    return {k: float(v) for k, v in zip(keys, stats)}

def frame(string: str, mode: str = 'block') -> str:
    '''Returns a printable shell frame.'''
    
    string = f'{FRAME[1]}{string}{FRAME[1]}'
    
    top = f"{FRAME[2]}{FRAME[0] * (len(string) - 2)}{FRAME[3]}"
    btm = f"{FRAME[4]}{FRAME[0] * (len(string) - 2)}{FRAME[5]}"
    
    # Init shell
    x, y = os.get_terminal_size()
    if mode == 'line': y = 4
    shell = [[' ' for _ in range(x)] for _ in range(y)]
    
    # Add string
    for i, chrs in enumerate(zip(top, string, btm)):
        
        for k, char in enumerate(chrs):
            # char = f'\033[92m{char}\033[0m' if char in COLOR else char
            
            esc = ''
            for seq, val in COLOR.items():
                if char in seq: esc = val
            
            shell[(y // 2) + k - 2][(x // 2) - len(string) + i] = f"{esc}{char}\033[0m"
            
    # Join
    return '\n'.join(map(''.join, shell))

def main() -> None:
    '''Runs Peung.'''
    
    # Fetch settings
    # mode = sys.argv[2] if len(sys.argv) > 2 else 'block'
    # speed = float(sys.argv[1]) if len(sys.argv) > 1 else 0.8
    
    mode = sys.argv[1] if len(sys.argv) > 1 else 'block'
    speed = 0.8
    
    # Loop
    try:
        while 1:
            print(frame(f"Ping: {round(ping()['avg'], 1)} ms", mode))
            time.sleep(speed)
    
    except KeyboardInterrupt: exit()

if __name__ == '__main__': main()