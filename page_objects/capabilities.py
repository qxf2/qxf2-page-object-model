import os
from conf import screenshot_conf
from datetime import datetime

class Capabilities:
    def saucelab_credentials(self, sauce_options,username,password):
        """Set saucelab credentials."""
        sauce_options['username'] = username
        sauce_options['accessKey'] = password
        return sauce_options

    def browserstack_credentials(self, browserstack_options,username,password):
        """Set browserstack credentials."""
        browserstack_options['userName'] = username
        browserstack_options['accessKey'] = password
        return browserstack_options

    def app_details(self, desired_capabilities, app_package, app_activity):
        desired_capabilities['appPackage'] = app_package
        desired_capabilities['appActivity'] = app_activity
        return desired_capabilities

    def app_name(self, desired_capabilities, app_path, app_name):
        desired_capabilities['app'] = os.path.join(app_path, app_name)
        return desired_capabilities

    def ios_capabilities(self, desired_capabilities, app_package, no_reset_flag, ud_id, org_id, signing_id):
        desired_capabilities['bundleId'] = app_package
        desired_capabilities['noReset'] = no_reset_flag
        if ud_id is not None:
            desired_capabilities['udid'] = ud_id
            desired_capabilities['xcodeOrgId'] = org_id
            desired_capabilities['xcodeSigningId'] = signing_id
        return desired_capabilities

    def saucelab_capabilities(self, desired_capabilities, app_name, username, password):
        desired_capabilities['appium:app'] = 'storage:filename='+app_name
        desired_capabilities['autoAcceptAlerts'] = 'true'
        sauce_mobile_options = {}
        sauce_mobile_options = self.saucelab_credentials(sauce_mobile_options,username, password)
        desired_capabilities['sauce:options'] = sauce_mobile_options
        return desired_capabilities

    def browserstack_capabilities(self, desired_capabilities, app_name, app_path, username, password, appium_version):
        bstack_mobile_options = {}
        bstack_mobile_options['idleTimeout'] = 300
        bstack_mobile_options['sessionName'] = 'Appium Python Test'
        bstack_mobile_options['appiumVersion'] = appium_version
        bstack_mobile_options['realMobile'] = 'true'
        bstack_mobile_options["networkProfile"] = "4g-lte-good"
        bstack_mobile_options = self.browserstack_credentials(bstack_mobile_options, username, password)
        desired_capabilities['app'] = self.browser_stack_upload(app_name, app_path) #upload the application to the Browserstack Storage
        desired_capabilities['bstack:options'] = bstack_mobile_options
        return desired_capabilities

    def browserstack_snapshots(self, desired_capabilities):
        desired_capabilities['debug'] = str(screenshot_conf.BS_ENABLE_SCREENSHOTS).lower()
        return desired_capabilities

    def set_os(self, desired_capabilities, os_name, os_version):
        """Set os name and os_version."""      
        desired_capabilities['os'] = os_name
        desired_capabilities['osVersion'] = os_version

        return desired_capabilities

    def remote_project_name(self, desired_capabilities, remote_project_name):
        """Set remote project name for browserstack."""
        desired_capabilities['projectName'] = remote_project_name

        return desired_capabilities

    def remote_build_name(self, desired_capabilities, remote_build_name):
        """Set remote build name for browserstack."""
        desired_capabilities['buildName'] = remote_build_name+"_"+str(datetime.now().strftime("%c"))

        return desired_capabilities

    def set_mobile_device(self, mobile_os_name, mobile_os_version, device_name):
        """Setup the mobile device."""
        desired_capabilities = {}
        desired_capabilities['platformName'] = mobile_os_name
        desired_capabilities['platformVersion'] = mobile_os_version
        desired_capabilities['deviceName'] = device_name

        return desired_capabilities