import mainbt
import os
import time
import threading

os.system('cls||clear')
print('Made by')
anim = ''' _                 _______  _______ 
( \      |\     /|(  ____ \(  ___  )
| (      | )   ( || (    \/| (   ) |
| |      | |   | || |      | (___) |
| |      | |   | || |      |  ___  |
| |      | |   | || |      | (   ) |
| (____/\| (___) || (____/\| )   ( |
(_______/(_______)(_______/|/     \|
                                    '''
for row in anim.split('\n'):
    print(row)
    time.sleep(0.03)
print('\n\n')

accs = os.listdir('accounts')

print(f"Running with {len(os.listdir('accounts'))} accounts in 5 seconds."); time.sleep(5)
os.system('cls||clear')
for raw_info in accs:
    items = raw_info.split('###')
    threading.Thread(target=mainbt.bot, args=(items[0], items[1], int(items[2]), items[3].replace('$$$', '.').replace('%%%', ':'))).start()
