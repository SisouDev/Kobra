from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVE_NAME = 'chromedriver.exe'
CHROMEDRIVE_PATH = ROOT_PATH / 'bin' / CHROMEDRIVE_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.ignore_local_proxy_environment_variables()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMEDRIVE_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('http://www.google.com/')
    sleep(5)
    browser.quit()

