![Python version](https://img.shields.io/badge/python-3.x-green?color=brightgreen)
![GitHub](https://img.shields.io/github/license/qxf2/qxf2-page-object-model?color=brightgreen)
![Maintenance](https://img.shields.io/maintenance/yes/2020?color=brightgreen)
[![CircleCI](https://circleci.com/gh/qxf2/qxf2-page-object-model.svg?style=shield)](https://circleci.com/gh/qxf2/qxf2-page-object-model)
[![BrowserStack Status](https://www.browserstack.com/automate/badge.svg?badge_key=T0U0cC9VRmk3RnZ3NHdhc3lYMHlqbEtIV0VvWXFuN25DeGhEdnhqTHJXVT0tLUMzQmV3cWVRaCtVSFhjZWtCeUdlOGc9PQ==--7a8a46022a744ab14de93e4d8970f7fbe520bec3)](https://www.browserstack.com/automate/public-build/T0U0cC9VRmk3RnZ3NHdhc3lYMHlqbEtIV0VvWXFuN25DeGhEdnhqTHJXVT0tLUMzQmV3cWVRaCtVSFhjZWtCeUdlOGc9PQ==--7a8a46022a744ab14de93e4d8970f7fbe520bec3)
![GitHub stars](https://img.shields.io/github/stars/qxf2/qxf2-page-object-model)
![GitHub forks](https://img.shields.io/github/forks/qxf2/qxf2-page-object-model)
![GitHub repo size](https://img.shields.io/github/repo-size/qxf2/qxf2-page-object-model)
![GitHub last commit](https://img.shields.io/github/last-commit/qxf2/qxf2-page-object-model)

--------
A Pythonic Selenium, Appium and API test automation framework
--------
You can use this test automation framework to write:

1. __Selenium__ and Python automation scripts to test web applications

2. __Appium__ and Python scripts for __mobile automation__ (Android and iOS)

3. __API automation__ scripts to test endpoints of your web/mobile applications

&nbsp;

![Qxf2 automation framework](https://qxf2.com/assets/img/framework_introduction.png)

&nbsp;

This GUI and API test automation framework is developed and maintained by [Qxf2 Services](https://qxf2.com). This framework is written in __Python__ and is based on the __Page Object Model__ - a design pattern that makes it easy to maintain and develop robust tests. We have also included our __API test automation framework__ based on the player-interface pattern in this repository. You can now write your API tests along with your Selenium and Appium tests.

We've implemented some version of this framework at several [clients](https://qxf2.com/clients). In all cases, this framework helped us write automated tests within the first week of our engagement. We hope you find this framework useful too!

If you end up using our framework, please let us know by giving us a star on GitHub and/or dropping an email to __mak@qxf2.com__

------
Setup
------

The setup for our open-sourced Python test automation framework is fairly simple. Don't get fooled by the length of this section. We have documented the setup instructions in detail so even beginners can get started.

The setup has four parts:

1. Prerequisites
2. Setup for GUI/Selenium automation
3. Setup for Mobile/Appium automation
4. Setup for API automation

__1. Prerequisites__

a) Install Python 3.x

b) Add Python 3.x to your PATH environment variable

c) If you do not have it already, get pip (NOTE: Most recent Python distributions come with pip)

d) pip install -r requirements.txt to install dependencies

If you ran into some problems on step (d), please report them as an issue or email Arun(mak@qxf2.com).


__2. Setup for GUI/Selenium automation__


a) Get setup with your browser driver. If you don't know how to, please try:

   > [For Chrome](https://sites.google.com/a/chromium.org/chromedriver/getting-started)

   > [For Firefox]( https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver)

#Note: Check Firefox version & Selenium version compatibility before downloading geckodriver.

__If your setup goes well__, you should be to run a simple test with this command:

1. Chrome: `python -m pytest -k example_form --browser Chrome`

2. Firefox: `python -m pytest -k example_form --browser Firefox`

__Optional steps__ for integrating with third-party tools:

* [Integrate our Python test automation framework with Testrail](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Testrail)
* [Integrate our Python GUI/web automation framework with BrowserStack ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Cloud-Services#browserstack)
* [Integrate our Python Selenium automation framework with Sauce Labs ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Cloud-Services#sauce-labs)
* [Run Python integration tests on Jenkins ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-CI-Tools#jenkins)
* [Run Python integration tests on CircleCI ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-CI-Tools#circleci)
* [Post Python automation test results on Slack ](https://github.com/qxf2/qxf2-page-object-model/wiki/Utilities#slack-integration)


__3. Setup for Mobile/Appium automation__


a) [Download and Install appium desktop app](https://github.com/appium/appium-desktop/releases/latest)

b) [Download and Install Android Studio and create an emulator](https://developer.android.com/studio/index.html)

c) [Install Java JDK](http://www.oracle.com/technetwork/java/javase/downloads/index.html)

d) [Install the appium Python client library](https://pypi.python.org/pypi/Appium-Python-Client)
pip install Appium-Python-Client

__If your setup goes well__, you should be to run a simple mobile test with this command after starting the Appium and Android emulator:
`python -m pytest -k mobile_bitcoin_price --mobile_os_version $Emulator_OS_Version --device_name $Emulator_Name`

__Optional steps__ for more details on setting up appium and running tests on Android or iOS refer to below links:
* [Get started with mobile automation: Appium & Python](https://qxf2.com/blog/appium-mobile-automation/)
* [Get Set Test an iOS app using Appium and Python](https://qxf2.com/blog/get-set-test-an-ios-app-using-appium-and-python/)


__4. Setup for API automation__

There are no extra setup steps for API automation. To verify, run test_api_example now using command "pytest -k api -s"

__Optional steps__ for more details on setting up API and running tests refer to below link:
* [Easily Maintainable API Test Automation Framework](https://qxf2.com/blog/easily-maintainable-api-test-automation-framework/)

-------------------
Repository details
-------------------
a) Directory structure of our current Templates

   ./

	|__conf: For all configurations and credential files

	|__log: Log files for all tests

	|__page_objects: Contains our Base Page, different Page Objects, DriverFactory, PageFactory

	|__endpoints: Contains our Base Mechanize, different End Points, API Player, API Interface

	|__screenshots: For screen shots

	|__tests: Put your tests in here

	|__utils: All utility modules (email_util,TestRail, BrowserStack, Base Logger, post_test_reports_to_slack) are kept in this folder


---------------------------
COMMANDS FOR RUNNING TESTS
---------------------------

a)py.test [options]

	-s	used to display the output on the screen			E.g: python -m pytest -s (This will run all the tests in the directory and subdirectories)
	--base_url  used to run against specific URL			E.g: python -m pytest --base_url http://YOUR_localhost_URL (This will run against your local instance)
	--remote_flag  used to run tests on Browserstack/Sauce Lab	E.g: python -m pytest -s --remote_flag Y -U https://qxf2.com
	--browser all	used to run the test against multiple browser 			E.g:python -m pytest ---browser all(This will run each test against the list of browsers specified in the conftest.py file,firefox and chrome in our case)
	--ver/-O	used to run against different browser versions/os versions	E.g: python -m pytest --ver 44 -O 8 (This will run each test 4 times in different browser version(default=45 & 44) and OS(default=7 & 8) combination)
	-h	help for more options 						E.g: python -m pytest -h
	-k      used to run tests which match the given substring expresion 	E.g: python -m pytest -k table  (This will trigger test_example_table.py test)
	--slack_flag	used to post pytest reports on the Slack channel		E.g: python -m pytest --slack_flag Y -v > log/pytest_report.log
	-n 	used to run tests in parallel					E.g: python -m pytest -n 3 -v (This will run three tests in parallel)
	--tesults 	used to report test results to tesults			E.g: python -m pytest test_example_form.py --tesults Y(This will report test report to tesults)

b)python tests/test_example_form.py (can also be used to run standalone test)

c)python tests/test_example_form.py --browser Chrome (to run against chrome)

d)python tests/test_api_example.py (make sure to run sample cars-api available at qxf2/cars-api repository before api test run)

e)python tests/test_mobile_bitcoin_price --mobile_os_version (android version) --device_name (simulator) --app_path (.apk location on local) --remote_flag Y (to run Mobile test case on Broswestack)remote_credentials.py
NOTE: For running tests in Browserstack, need to update Username/Accesskey from Browserstack Account to remote_credentials.py under conf.

--------
ISSUES?
--------

a) If Python complains about an "Import" exception, please 'pip3 install $module_name'

b) If you don't have drivers set up for the web browsers, you will see a helpful error from Selenium telling you where to go and get them

c) If your are using firefox 47 and above, you need to set up Geckodriver. Refer following link for setup: https://qxf2.com/blog/selenium-geckodriver-issue/

d) On Ubuntu, you may run into an issue installing the cryptography module. You need to `sudo apt-get install libssl-dev` and then run `sudo pip install -r requirements.txt`

-----------
Continuous Integration and Support
-----------
This project uses:
<a href="https://www.browserstack.com/"><img src="http://www.browserstack.com/images/layout/browserstack-logo-600x315.png" width="150" height="100" hspace="10"></a>
<a href="https://circleci.com/"><img src="https://github.com/circleci/media/blob/master/logo/build/horizontal_dark.1.png?raw=true" width="150" height="100" hspace="10"></a>


 1. [BrowserStack](https://www.browserstack.com) for testing our web and mobile based tests on cloud across different platform and browsers.

 2. [CircleCI](https://circleci.com/) for continuous integration.

-----------
NEED HELP?
-----------
Struggling to get your GUI automation going? You can hire Qxf2 Services to help. Contact us at mak@qxf2.com