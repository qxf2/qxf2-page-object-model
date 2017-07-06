--------
Welcome
--------
This repository contains Qxf2 Services's test automation framework. You can use this to write your Selenium and Appium tests. We love Python - so this framework is written completely in Python. Our framework is based on the Page Object pattern - a design pattern that makes maintaining and developing robust tests easy. 


We've implemented some version of this framework at several clients (https://qxf2.com/clients). In all cases, the framework helped us write automated tests within the first week of our engagement. We hope you find this framework useful too!


---------
SETUP
---------

a) Install Python 2.x

b) Add Python 2.x to your PATH environment variable

c) If you do not have it already, get pip (NOTE: Most recent Python distributions come with pip)

d) `pip install -r requirements.txt` to install dependencies

e) Get setup with your browser driver. If you don't know how to, please try:

   > For Chrome: https://sites.google.com/a/chromium.org/chromedriver/getting-started

   > For Firefox: https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver	#Note: Check firefox version & selenium version compatibility before downloading geckodriver.

f) [ADVANCED and OPTIONAL] Update 'conf/remote_credentials.py' if you want to run on BrowserStack/Sauce Labs

g) [ADVANCED and OPTIONAL] In case you have TestRail Integration update the 'conf/testrail.conf' with proper case ids. Also update the 'conf/testrail.env' with url,user,password.

h) [ADVANCED and OPTIONAL] Refer 'utils/post_test_reports_to_slack.py'and add slack incoming webhook url if you want to post the test reports on Slack channel.


__If your setup goes well__, you should be to run a simple test with this command:

1. Chrome: `python tests/test_example_form.py -B Chrome` 

2. Firefox: `python tests/test_example_form.py -B Firefox`



-------------------
Repository details
-------------------
a) Directory structure of our current Templates

   ./

	|__conf: For all configurations and credential files

	|__log: Log files for all tests

	|__page_objects: Contains our Base Page, different Page Objects, DriverFactory, PageFactory

	|__screenshots: For screen shots

	|__tests: Put your tests in here

	|__utils: All utility modules (email_util,TestRail, BrowserStack, Base Logger, post_test_reports_to_slack) are kept in this folder
	

---------------------------
COMMANDS FOR RUNNING TESTS
---------------------------

a)py.test [options]

	-s	used to display the output on the screen			E.g: py.test -s (This will run all the tests in the directory and subdirectories)
	-U  	used to run against specific URL				E.g: py.test -U http://YOUR_localhost_URL (This will run against your local instance)
	-M  	used to run tests on Browserstack/Sauce Lab			E.g: py.test -s -M Y -U https://qxf2.com	
	-B all	used to run the test against multiple browser 			E.g: py.test -B all(This will run each test against the list of browsers specified in the conftest.py file,firefox and chrome in our case)
	-V/-O	used to run against different browser versions/os versions	E.g: py.test -V 44 -O 8 (This will run each test 4 times in different browser version(default=45 & 44) and OS(default=7 & 8) combination)
	-h	help for more options 						E.g: py.test -h
	-k      used to run tests which match the given substring expresion 	E.g: py.test -k table  (This will trigger test_example_table.py test)
	-I	used to post pytest reports on the Slack channel		E.g: py.test -I Y -v > log/pytest_report.log
	-n 	used to run tests in parallel					E.g: py.test -n 3 -v (This will run three tests in parallel)

b)python tests/test_example_form.py (can also be used to run standalone test) 	

c)python tests/test_example_form.py -B Chrome (to run against chrome)

--------
ISSUES?
--------

a) If Python complains about an Import exception, please 'pip install $module_name'

b) If you are not setup with the drivers for the web browsers, you will see a helpful error from Selenium telling you where to go and get them

c) If your are using firefox 47 and above, you need to setup with Geckodriver. Refer following link for setup: https://qxf2.com/blog/selenium-geckodriver-issue/

d) On Ubuntu, you may run into an issue installing the cryptography module. You need to `sudo apt-get install libssl-dev` and then run `sudo pip install -r requirements.txt`

-----------
NEED HELP?
-----------
Are you struggling to get your GUI automation going? You can hire Qxf2 Services to help. Contact us at mak@qxf2.com