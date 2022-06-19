import praw
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pickle
import time
from random import choice
from random import choices
import string

global usernames
with open('uns.txt', 'r') as f:
    usernames = f.readlines()
login = 'lfoUzJIx0BHO6sql_vY3Nw:2CjpILCo664VFWccJKGo9JiGiHEMOQ:Reddit1!:OF LeakZ (by u/leakz0ne):leakz0ne'.split(':')

reddit = praw.Reddit(
    client_id = login[0],
    client_secret = login[1],
    password = login[2],
    user_agent = login[3],
    username = login[4]
)

def driver_setup():
    global chromeOptions
    chromeOptions = Options()
    chromeOptions.add_argument("--headless") 
    chromeOptions.add_argument("--disable-setuid-sandbox")
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
    chromeOptions.add_argument("--disable-dev-shm-using") 
    chromeOptions.add_argument("--disable-extensions") 
    chromeOptions.add_argument("--disable-gpu") 
    chromeOptions.add_argument("disable-infobars")
    chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chromeOptions.add_argument("--no-sandbox")
def manual():
    while True:
        startup_option = int(input('Pick action:\n[1] Account setup\n[2] Start bot\n'))
        if startup_option == 1:
            account_setup()
            break
        elif startup_option == 2:
            for index, acc in enumerate(os.listdir('accounts')):
                print(f'''[{index+1}] {acc.split('###')[0]}''')
            account_option = os.listdir(os.path.join('./accounts'))[int(input('Pick an account: '))-1].split('###')
            #open(os.path.join('./monomer-b', xyz)).read()
            bot(account_option[0], account_option[1], int(account_option[2]), account_option[3].replace('$$$', '.').replace('%%%', ':'))
            break
def account_setup():
    while True:
        username = input('\nUsername: ')
        password = input('Password: ')
        port = input('Webdriver port: ')
        proxy = input('Account proxy: ')
        print(f'\n\nSetting up {username}...')
        driver_setup()
        driver = webdriver.Chrome('chromedriver', options=chromeOptions, port=int(port))
        driver.get('https://old.reddit.com/login')
        driver.find_element(By.XPATH, '//input[@id="user_login"]').send_keys(username)
        driver.find_element(By.XPATH, '//input[@id="passwd_login"]').send_keys(password)
        driver.find_element(By.XPATH, '//button[@tabindex="3"]').click()
        WebDriverWait(driver, float('inf')).until(EC.presence_of_element_located((By.XPATH, '//div[@id="siteTable"]')))
        #open(os.path.join('./monomer-b', xyz)).read()
        pickle.dump(driver.get_cookies(), open(os.path.join('./accounts', f'''{username}###{password}###{port}###{proxy.replace('.', '$$$').replace(':', '%%%')}'''),"wb"))
        print(f'Account {username} successfully saved.\n')
        
def bot(user, pw, port, proxy):
    driver_setup()
    ID = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
    print(f'Assigned ID {ID}\n')
    chromeOptions.add_argument("window-size=600,1080")
    webdriver.DesiredCapabilities.CHROME['proxy'] = {"httpProxy": proxy, "ftpProxy": proxy, "sslProxy": proxy, "proxyType": "MANUAL",}
    driver = webdriver.Chrome('chromedriver', options=chromeOptions)
    with open('msgs.txt', 'r') as f:
        msgs = f.readlines()
    with open('subs.txt', 'r') as f:
        subs = f.readlines()
    cookies = pickle.load(open(os.path.join('./accounts', f'''{user}###{pw}###{str(port)}###{proxy.replace('.', '$$$').replace(':', '%%%')}'''), 'rb'))
    driver.get('https://old.reddit.com/')
    for item in cookies:
        driver.add_cookie(item)
    while True:
        sub = choice(subs)
        print(f'\n{ID}: /r/{sub}')
        driver.get('https://old.reddit.com/r/'+sub+'/new')
        try:
            driver.find_element('//div[@class="insterstitial"]/img[@class="interstitial-image"]')
            continue
        except:
            pass
        try:
            driver.find_element(By.XPATH, '//div[@class="buttons"]/button[@value="yes"]').click()
        except:
            pass
        WebDriverWait(driver, float('inf')).until(EC.presence_of_element_located((By.XPATH, '//a[@data-event-action="title"]')))
        raw = driver.find_elements(By.XPATH, '//li[@class="first"]//a')
        href = []
        for rw in raw[1:]:
            href.append(rw.get_attribute('href'))
        del raw
        print(f'\n{ID}: Starting cycle of {len(href)} threads')
        for thread in href[1:]:
            for com in list(reddit.submission(id=thread.split('/')[-3]).comments):
                if com.author in usernames:
                    print(f'{ID}: Already replied')
                    continue
            driver.get(thread)
            try:
                driver.switch_to.alert.accept()
            except:
                pass
            WebDriverWait(driver, float('inf')).until(EC.presence_of_element_located((By.XPATH, '//textarea[@data-event-action="comment"]')))
            driver.find_element(By.XPATH, '//textarea[@data-event-action="comment"]').send_keys(choice(msgs))
            #driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            print(f'{ID}: Submitted post')
            time.sleep(600) #DELAY
        print(f'{ID}: Completed cycle')

if __name__ == '__main__':
    manual()
