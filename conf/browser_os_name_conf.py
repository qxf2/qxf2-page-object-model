"""
Conf file to generate the cross browser cross platform test run configuration
"""

#Conf list for local
default_browser = ["firefox"]  #default browser for the tests to run against when -B option is not used
local_browsers = ["firefox","chrome"]  #local browser list against which tests would run if no -M y option is used


#Conf list for Browserstack/Sauce Labs
#change this depending on your client
browsers = ["firefox","chrome"]  #browsers to generate test run configuration to run on Browserstack/Sauce Labs
firefox_versions = ["45","46"]  #firefox versions for the tests to run against on Browserstack/Sauce Labs
chrome_versions = ["49","50"]  #chrome versions for the tests to run against on Browserstack/Sauce Labs
os_list = ["windows","OS X"]   #list of os for the tests to run against on Browserstack/Sauce Labs
windows_versions = ["7","8.1"] #list of windows versions for the tests to run against on Browserstack/Sauce Labs
os_x_versions = ["yosemite"]   #list of os x versions for the tests to run against on Browserstack/Sauce Labs
default_config_list = [("firefox","45","windows","7")] #default configuration against which the test would run if no -B all option is used


def generate_configuration(browsers=browsers,firefox_versions=firefox_versions,chrome_versions=chrome_versions,
							os_list=os_list,windows_versions=windows_versions,os_x_versions=os_x_versions):

	"Generate test configuration"
	test_config = []
	for browser in browsers:
		if browser == "firefox":
			for firefox_version in firefox_versions:
				for os_name in os_list:
					if os_name == "windows":
						for windows_version in windows_versions:
							config = [browser,firefox_version,os_name,windows_version]
							test_config.append(tuple(config))
					if os_name == "OS X":
						for os_x_version in os_x_versions:
							config = [browser,firefox_version,os_name,os_x_version]
							test_config.append(tuple(config))
		if browser == "chrome":
			for chrome_version in chrome_versions:
				for os_name in os_list:
					if os_name == "windows":
						for windows_version in windows_versions:
							config = [browser,chrome_version,os_name,windows_version]
							test_config.append(tuple(config))
					if os_name == "OS X":
						for os_x_version in os_x_versions:
							config = [browser,chrome_version,os_name,os_x_version]
							test_config.append(tuple(config))



	return test_config

#variable to hold the configuration that can be imported in the conftest.py file
cross_browser_cross_platform_config = generate_configuration()



