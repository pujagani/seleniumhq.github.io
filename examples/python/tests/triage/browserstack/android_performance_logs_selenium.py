import json

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common import keys, desired_capabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

username = ''
accessKey = ''

options = ChromeOptions()
# options.set_capability('chromeOptions', {
#     'perfLoggingPrefs': {
#         'enableNetwork': True,
#         'enablePage': True,
#         'enableTimeline': True,
#         'traceCategories': 'devtools.timeline,devtools.network,devtools.cpu'
#     }
# })
options.set_capability('enablePerformanceLogging',True)
options.set_capability('enableNetwork',True)
options.set_capability('interactiveDebugging',True)
#options.add_argument(f'loggingPrefs={str({'browser': 'ALL'})}'))

options.set_capability('appium:chromeLoggingPrefs', {'performance': 'ALL'})
options.set_capability('acceptInsecureCerts', True)
#options.set_capability('pageLoadStrategy', 'none')
options.set_capability('ignoreCertificateErrors', True)
options.add_argument("--allow-running-insecure-content")
options.add_experimental_option("w3c", False)

bstack_options = {
        'geoLocation': 'GB',
        'idleTimeout': '300',
        'consoleLogs': 'verbose',
        'os': 'Android',
        'deviceName': 'Samsung Galaxy S23',
       # 'osVersion': 12,
        'browserName': 'Chrome',
        'interactiveDebugging': True,
        'telemetryLogs': True,
        'disableCorsRestrictions': True,
        'browserstack.networkLogs': True
    }
options.set_capability('bstack:options', bstack_options)
driver = webdriver.Remote(options=options,
                          command_executor="https://" + username + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub")

# Hack the Logging API into the Python remote driver.
# Not implemented in Selenium, patch welcome!!
driver.command_executor._commands.update({
    'getAvailableLogTypes': ('GET', '/session/$sessionId/log/types'),
    'getLog': ('POST', '/session/$sessionId/log')})

try:
  driver.get('http://beta-sports.ladbrokes.com/buildInfo.json?automationtest=true')

  print('Available log types:', driver.execute('getAvailableLogTypes')['value'])

  for log_entry in driver.get_log("performance"):
      log_message = json.loads(log_entry["message"])["message"]

  print('Profiler log:', driver.execute('getLog', {'type': 'performance'})['value'])

finally:
  driver.quit()