import os

from selenium.webdriver import DesiredCapabilities


def __start_browser_stack(self, maximized=False):
    os.environ['USE_FW_PROXY'] = "true"
    self.browser_opts = ChromeOptions()
    capabilities_map = {
        "firefox": DesiredCapabilities.FIREFOX,
        "opera": DesiredCapabilities.OPERA,
        "chrome": DesiredCapabilities.CHROME,
        "ie": DesiredCapabilities.INTERNETEXPLORER,
        "edge": DesiredCapabilities.EDGE,
        "safari": DesiredCapabilities.SAFARI,
        "iphone": DesiredCapabilities.IPHONE,
        "ipad": DesiredCapabilities.IPAD,
        "android": DesiredCapabilities.ANDROID,
        "samsung": DesiredCapabilities.ANDROID
    }
    desired = capabilities_map.get(self.browser, DesiredCapabilities.CHROME)
    self.add_browser_args(options=self.cmd_line_args)
    if (self.type == 'mobile' and not 'iPhone' in self.device_args.get('device')) or (self.type == 'desktop'):
        self.add_browser_args(options='user-agent=%s' % self.user_agent)
    else:
        if self.bs_log_config.get('networkLogs'):
            desired['browserstack.networkLogs'] = self.bs_log_config.get('networkLogs')
            desired['browserstack.networkLogsOptions'] = {
                'captureContent': self.bs_log_config.get('networkLogs'),
            }
    # self.add_browser_args(options='window-size=%s,%s' % (self.width, self.height))
    all_blocked_hosts = tests.settings.blocked_hosts + self.blocked_hosts
    if all_blocked_hosts:
        self.add_browser_args(options=self.prepare_host_rules_option(all_blocked_hosts))
    self.browser_opts.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    })
    if (get_device_properties()['browser'].lower() in ['safari', 'chromium'] and
            'iphone' in get_device_properties()['device'].lower()):
        desired['browserstack.headerParams'] = json.dumps({
            "User-Agent": self.user_agent
        })
    self.browser_opts.add_experimental_option('excludeSwitches', ['enable-automation'])
    desired['acceptSslCerts'] = True
    desired['pageLoadStrategy'] = 'none'
    desired['browserstack.geoLocation'] = 'GB'
    desired['browserstack.idleTimeout'] = '300'
    desired['browserstack.debug'] = self.bs_log_config.get('debug', False)
    desired['browserstack.video'] = self.bs_log_config.get('video', False)
    # Reverting to default
    # desired['browserstack.seleniumLogs'] = self.bs_log_config.get('seleniumLogs', False)
    # desired['browserstack.appiumLogs'] = self.bs_log_config.get('appiumLogs', False)
    desired['browserstack.console'] = self.bs_log_config.get('console', False)
    if self.enable_bs_performance_log:
        desired['enablePerformanceLogging'] = False if self.type == 'mobile' and 'iPhone' in self.device_args.get(
            'device') else True
    desired['disableAndroidSoftKeyboard'] = True
    desired['interactiveDebugging'] = True
    desired['browserName'] = self.device_args.get('browser')
    desired['os'] = self.os.upper()
    desired['os_version'] = self.device_args.get('os_version')
    desired['device'] = self.name
    desired['framework'] = 'pytest'

    if tests.location == "AWS_GRID":
        logging.info(f"Local browser Build name: {tests.build_name}")
        if tests.build_name and tests.build_name != "None":
            ci_run_number = os.environ.get('BUILD_NUMBER', None)
            desired['build'] = f"{tests.build_name} BUILD_NUMBER:{ci_run_number}"
        else:
            ci_run_name = os.environ.get('JOB_NAME', None)
            ci_run_number = os.environ.get('BUILD_NUMBER', None)
            git_branch = os.environ.get('GIT_BRANCH', None)
            hostname = os.environ.get('OX_HOSTNAME', None)
            test_run_name = f'Automation Run {ci_run_name} BUILD_NUMBER:{ci_run_number}{f" [{git_branch}]" if git_branch else ""} @ {hostname}'
            desired['build'] = test_run_name
    else:
        if tests.build_name:
            desired['build'] = tests.build_name
    if self.proxy is not None:
        self.add_browser_args(options='proxy-server=%s' % self.proxy)
    if self.chrome_profile is not None:
        self.add_browser_args(options='user-data-dir=%s' % self.chrome_profile)
    try:
        if self._browser_stack_driver.get('command_executor'):
            desired['resolution'] = '1280x800'
            driver = self._browser_stack_driver['type'](
                command_executor=self._browser_stack_driver['command_executor'].format(
                    username=tests.bs_username,
                    access_key=tests.bs_access_key),
                desired_capabilities=desired,
                options=self.browser_opts,
                keep_alive=True)
        else:
            raise DeviceException('Command executor is not provided for BrowserStack')
        # if self.type == 'mobile':
        #     if self._browser_stack_mobile_driver.get('command_executor'):
        #         driver = self._browser_stack_mobile_driver['type'](
        #             command_executor=self._browser_stack_mobile_driver['command_executor'],
        #             desired_capabilities=desired,
        #             keep_alive=True)
        #     else:
        #         raise DeviceException('Command executor is not provided for BrowserStack')
        # else:
        #     if self._browser_stack_driver.get('command_executor'):
        #         desired['resolution'] = '1280x800'
        #         driver = self._browser_stack_driver['type'](
        #             command_executor=self._browser_stack_driver['command_executor'],
        #             desired_capabilities=desired,
        #             options=self.browser_opts,
        #             keep_alive=True)
        #     else:
        #         raise DeviceException('Command executor is not provided for BrowserStack')
    except URLError as e:
        raise DeviceException('Cannot start appium driver. Error:  "URLError: %s"' % e.reason)
    if maximized:
        driver.maximize_window()
    return driver