from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import sys
import time
import argparse
import pyfiglet
import random
import string
from termcolor import colored, cprint

import openai
import json

#setup first https://www.usessionbuddy.com/post/How-To-Install-Selenium-Chrome-On-Centos-7/
############
### Modify this with your API Key

openai.api_key = ""
url_owa = "https://example.com:8090/snappymail"
credentials_list = [
    {"sajetek@example.com": "ExampleP@$$"},
    {"sajetek2@example.com": "ExampleP@$$2"},
    # ... more email-password pairs
]

############

def if_exists(el, id_or_class):

    return False
    
    driver.implicitly_wait(0)
    if id_or_class == "id":
        exists = driver.find_element(By.ID, el)
    else:
        exists = driver.find_element(By.CLASS_NAME, el)
    driver.implicitly_wait(3)
    return exists
    
def random_word():
    # Generates a random word of length 3 to 6 consisting of random letters
    word_length = random.randint(3, 6)
    word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_length))
    return word

def random_sentence():
    # Generates a random sentence of up to 30 words
    sentence_length = random.randint(15, 30)
    sentence = ' '.join(random_word() for _ in range(sentence_length))
    return sentence.capitalize() + '.'

def send_owa_email(owa_login, owa_pass, email_list, counter, flag, email_mode):
    print("[+] Visiting SaJeTek Portal", end='\r\n')
    driver.get(url_owa)
    time.sleep(7)

    print("[+] Logging into SaJeTek as {0}".format(owa_login), end='\r\n')
    
    driver.find_element(By.NAME, "Email").send_keys(owa_login)
    driver.find_element(By.NAME, "Password").send_keys(owa_pass)
    driver.find_element(By.CLASS_NAME, "buttonLogin").click()
    time.sleep(7)
    
    try:
        element = driver.find_element(By.CLASS_NAME, "buttonLogin")
        print("[+] Authentication was NOT successful", end='\r\n')
        sys.exit()
    except NoSuchElementException:
        print("[+] Authenticated successfully", end='\r\n')

    else:
        email_to = email_list[0]
    
    if flag == 0:
        print("[+] Composing emails for {0}".format(email_list[0]), end='\r\n')

    subject_list = ["Weekend plans", "Happy holidays!", "Last weeks discussion", "Plan for the trip", "Team Celebrations", "Travel Itinary for Next Month", "Lunch Date", "Whiteboard Meeting Call","A few things to celebrate this week", "Debrief Call - Project Completed", "Quote for new opportunity", "Leave Details Request"]
    body_list = ["Hey there,\n\nJust wanted to check in and see if you're up for some weekend fun? I was thinking of hitting up the farmers market on Saturday and then grabbing lunch. Let me know if you're interested.", "Hey,\n\nI just wanted to wish you a happy birthday and let you know how grateful I am to have you in my life. Hope you have a great day. Cheers!", "Hi there,\n\nIt's been a while since we caught up! I was thinking of grabbing lunch next week, would you be free on Wednesday or Thursday? Let me know!\n\nRegards,\nJen", "Hi,\n\nI saw on LinkedIn that you got a promotion, congrats! I know how hard you've been working and you deserve it. Let's grab drinks to celebrate soon. Cheers!", "Hi there,\n\nHope you're doing well. I had a quick question about that project we worked on last month. Would you mind hopping on a call sometime this week to chat about it? D.", "Hey,\n\nI know you've traveled to Paris before and I was wondering if you had any tips or recommendations for my upcoming trip. I'd love to hear your thoughts. J.", "Hey,\n\nJust wanted to wish you and your family a happy holiday season! Hope you get to enjoy some time off and relaxation.", "Hi, All,\n\nJust summarising the call today:\nProcessor is only 2kb so Mark has suggested we do CTF type challenges. D", "Hi Everyone,\n\nA few things for us to celebrate this week:\n\n Owen is celebrating his birthday on Thursday\n Jess will be celebrating his 1st work anniversary on Friday\n\nBest wishes to you both, from your friends in WKL"]
 
    i = 1
    tots_sent = counter

    while i <= counter:

        if email_mode == '1':
            email_subject = ' '.join(random_word() for _ in range(3))
            email_message = "Hi there,\n\n" + random_sentence() + "\n" + random_sentence() + random_sentence() + "\n\n" + random_sentence()
        
        elif email_mode == '2':
            email_subject = random.choice(subject_list) # Removed support for OpenAI to avoid unnecessary costs
            email_message = askGPT()

        else:
            email_subject = random.choice(subject_list)
            email_message = random.choice(body_list)
        
        try:

            if flag == 1:
                email_to = email_list[i-1]
                print("[+] Composing emails for {0}".format(email_to))

            else:
                email_to = email_list[0]
            
            #Open compose window
            driver.find_element(By.CLASS_NAME, "buttonCompose").click()
            time.sleep(2)
		
            driver.find_element(By.CSS_SELECTOR, "#V-PopupsCompose .emailaddresses-input input").send_keys(email_to)
            driver.find_element(By.CSS_SELECTOR, "#V-PopupsCompose .emailaddresses-input input").send_keys(Keys.RETURN)
            driver.find_element(By.NAME, "subject").send_keys(email_subject)
            driver.find_element(By.CLASS_NAME, "squire-wysiwyg").send_keys(email_message)
            time.sleep(2)

            driver.find_element(By.CSS_SELECTOR, "#V-PopupsCompose .btn-success").click()
            time.sleep(2)

            print("[+] Counter: {0}".format(i), end='\r\n')

        except Exception as e:

             print("[!] Error on Counter {0}: {0}".format(i, e))
             print(f"An exception occurred: {e}")
             tots_sent -=1

        i += 1
        time.sleep(8)

    print("[+] {0} emails completed".format(tots_sent))
    print("[+} Logging out..", end='\r\n')    

    driver.find_element(By.ID, "top-system-dropdown-id").click()
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, "#V-SystemDropDown .dropdown-menu [data-i18n='GLOBAL/LOGOUT']").click()
    time.sleep(3)

    print("[+] Logged out successfully", end='\r\n')
    time.sleep(1)


def askGPT():

    if openai.api_key == "":
        print("[!] OpenAI API key is required.")

    prompt_text = "Write a typical corporate email without a subject in 50 words that do not use any words that may trigger spam controls. Begin with the body without any trail spaces or new lines, and sign off with two new lines, followed by the name Bob at the end"
    response = openai.Completion.create( engine="text-davinci-002", prompt=prompt_text, temperature=0.6,  max_tokens=150 )
    generated_text = response.choices[0].text
    return generated_text

def read_credentials(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the first line as username
            username = file.readline().strip()
            
            # Read the second line as password
            password = file.readline().strip()
            
            return username, password
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
        
# Main
prebanner = pyfiglet.figlet_format("Warmer")
VERSION = colored('VERSION: 1.0 \n\n-- Written by @Firestone65, modified by SaJeTek-Developer for Cyberpanel snappymail --\n', 'red', attrs=['bold'])
'Sender reputation warmer for phishing campaigns'
banner = prebanner + "\n" + VERSION
print(banner)

parser = argparse.ArgumentParser(description= '[+] Sender reputation warmer for phishing campaigns')
parser.add_argument('-u', type=str, required=False, help='Sender Email ID')
parser.add_argument('-p', type=str, required=False, help='Sender Email Password')
parser.add_argument('-T', type=str, dest="T", required=False, help='Single Target Email ID')
parser.add_argument('-t', type=str, dest="t", required=False, help='Multiple Targets from Wordlist')
parser.add_argument('-x', type=int, required=False, help='No. of Emails to Send (applicable only for single targets)')
parser.add_argument('-m', type=str, required=True, help='Email Content Mode [ 1, 2, 3] where 1 = Gibberish sentence, 2 = AI-Generated, 3 = Randomly choose from pre-defined templates')
args = parser.parse_args()

# Distinguish between single vs. multiple recipients
flag = 0

#Email Information
email_list = list()

if args.t is not None:
    emails_txt = args.t

    with open(emails_txt, 'r') as fp:
        
        flag = 1
        email_list = [line.rstrip('\n') for line in fp.readlines()]
        send_volume = len(email_list)


elif args.T is not None:
    email_list.append(args.T)
    
    if args.x is not None:
        send_volume = args.x
    else:
        print("[!] Send volume not provided. Defaulting to 1 email")
        send_volume = 1

else:
    print("[!] Required fields: Target Email ID / Target Email Wordlist")
    sys.exit()

email_mode = args.m

email_login = args.u
email_pass = args.p

# Initialize Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--no-sandbox')
options.add_argument('--disable-smooth-scrolling')
options.add_argument('disable-notifications')
options.add_argument("window-size=1280,720")
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
driver.maximize_window()

if email_login is not None && if email_pass is not None:
    send_owa_email(email_login, email_pass, email_list, send_volume, flag, email_mode)

#process list
for credentials in credentials_list:
    for email_login, email_pass in credentials.items():
        send_owa_email(email_login, email_pass, email_list, send_volume, flag, email_mode)

print("\n[+] Automation complete", end='\r\n')
#inp = input('\n ---- Hit any key to quit')

driver.quit()
