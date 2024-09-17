from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common import keys, desired_capabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

username = ''
accessKey = ''

options = ChromeOptions()
options.set_capability('enablePerformanceLogging',True)
options.set_capability('enableNetwork',True)
options.set_capability('interactiveDebugging',True)

options.set_capability('goog:loggingPrefs', {'browser': 'INFO', 'performance': 'ALL'})

#options.set_capability('goog:chromeOptions.perfLoggingPrefs', {'enableNetwork',True})
options.set_capability('acceptInsecureCerts', True)
options.set_capability('ignoreCertificateErrors', True)
options.add_argument("--allow-running-insecure-content")

bstack_options = {
       # 'geoLocation': 'GB',
        'idleTimeout': '300',
        'consoleLogs': 'verbose',
        'os': 'Android',
        'deviceName': 'Samsung Galaxy S22',
       'osVersion': 12,
        'browserName': 'Chrome',
        'interactiveDebugging': True,
        'telemetryLogs': True,
        'disableCorsRestrictions': True,
        'wsLocalSupport': True,
    }
options.set_capability('bstack:options', bstack_options)
driver = webdriver.Remote(options=options,
                          command_executor="https://" + username + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub")

driver.command_executor._commands.update({
    'getAvailableLogTypes': ('GET', '/session/$sessionId/se/log/types'),
    'getLog': ('POST', '/session/$sessionId/se/log')
})

try:
  driver.get('https://www.selenium.dev')

  print('Available log types:', driver.execute('getAvailableLogTypes')['value'])

  # network_info = driver.execute_script("var performance = window.performance || window.mozPerformance || "
  #                                      "window.msPerformance || window.webkitPerformance || {}; var network = "
  #                                      "performance.getEntries() || {}; return network;")
  # print(network_info)
finally:
  driver.quit()