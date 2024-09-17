import json

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# Set Chrome options and desired capabilities
options = webdriver.ChromeOptions()
# options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Frontend-Automation')
# Set the performance logging preferences
perf_logging_prefs = {
    'enableNetwork': True,
    'enablePage': True,
    'traceCategories': 'devtools.timeline,devtools.network,devtools.cpu'
}
# options.add_experimental_option('perfLoggingPrefs', perf_logging_prefs)

# Set desired capabilities for Chrome
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['enablePerformanceLogging'] = True
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
capabilities['acceptInsecureCerts'] = True
capabilities['disableAndroidSoftKeyboard'] = True
capabilities['interactiveDebugging'] = True
capabilities["os_version"] = "13.0"
capabilities['os'] = 'ANDROID'
# capabilities['chromeOptions'] = options.to_capabilities()['goog:chromeOptions']

# Set BrowserStack options
bstack_options = {
    'geoLocation': 'GB',
    # 'consoleLogs': 'verbose',
    'browserName': 'Chrome',
    'interactiveDebugging': True,
    # 'telemetryLogs': True,
    # 'useW3C': False,
}
# capabilities['bstack:options'] = bstack_options
for key,val in bstack_options.items():
    capabilities[f'browserstack.{key}'] = val
capabilities['device'] = 'Samsung Galaxy S23'

# Initialize the Remote WebDriver
driver = webdriver.Remote(
    command_executor="https://" + "pujajagani1" + ":" + "quy1Djunpp3REqy9RDcn" + "@hub-cloud.browserstack.com/wd/hub",
    desired_capabilities=capabilities,
    keep_alive=True,
)

driver.command_executor._commands.update({
    'getAvailableLogTypes': ('GET', '/session/$sessionId/se/log/types'),
    'getLog': ('POST', '/session/$sessionId/se/log')
})

try:
    driver.get('http://beta-sports.ladbrokes.com/buildInfo.json?automationtest=true')

    print('Available log types:', driver.execute('getAvailableLogTypes')['value'])

    for log_entry in driver.get_log("performance"):
        log_message = json.loads(log_entry["message"])["message"]

    print('Profiler log:', driver.execute('getLog', {'type': 'performance'})['value'])

finally:
    driver.quit()