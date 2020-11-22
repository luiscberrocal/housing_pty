import time
from selenium import webdriver
from shutil import which
#❯ PATH=$PATH:/Users/luiscberrocal/PycharmProjects/pty_housing/chrome_driver_86/chromedriver
import os

from selenium.webdriver.chrome.options import Options

t = os.getenv('PATH')
chrome_options = Options()


print(f'path: {t}')
driver = webdriver.Chrome(executable_path='/Users/luiscberrocal/PycharmProjects/pty_housing/chrome_driver_86/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
#search_box = driver.find_element_by_name('q')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
driver.close()