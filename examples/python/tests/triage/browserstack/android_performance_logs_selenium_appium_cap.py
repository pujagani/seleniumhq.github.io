import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

username = ''
accessKey = ''

# Set up BrowserStack options
browserstack_options = {
    "os": "Android",
    "deviceName": "Samsung Galaxy S22",
    "osVersion": "12",
    "sessionName": "Console Logs",
    "browserstack.networkLogs": True,
    "appiumVersion": "2.4.1"
}

# Set up Chrome options
chrome_options = Options()

# Set up logging preferences
log_prefs = {
    'performance': 'ALL'
}

# Add logging preferences to Chrome options specific to Appium
# This is the fix
chrome_options.set_capability('appium:chromeLoggingPrefs', log_prefs)

# Add BrowserStack options to Chrome options
chrome_options.set_capability('bstack:options', browserstack_options)

# Initialize the WebDriver
driver = webdriver.Remote(
    command_executor="https://" + username + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub",
    options=chrome_options
)

# Open a website
driver.get("http://beta-sports.ladbrokes.com/buildInfo.json?automationtest=true")

# Print available log types
print(driver.log_types)

# Retrieve and print performance logs
for entry in driver.get_log('performance'):
    print(entry)

# Quit the driver
driver.quit()