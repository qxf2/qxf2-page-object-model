--------
A Pythonic Selenium and Appium test automation framework
--------
You can use this test automation framework to write:

1. __Selenium__ and Python automation scripts to test web applications

2. __Appium__ and Python scripts for __mobile automation__ (Android and iOS) 

3. API automation scripts to test endpoints of your web/mobile applications

This GUI and API test automation framework is developed and maintained by [Qxf2 Services](https://qxf2.com). This framework is written in __Python__ and is based on the __Page Object Model__ - a design pattern that makes it easy to maintain and develop robust tests. We have also included our __API test automation framework__ based on the player-interface pattern in this repository. You can now write your API tests along with your Selenium and Appium tests. Please note: the API test examples are written for the sample API available at [Cars API](https://github.com/qxf2/cars-api) repository.

We've implemented some version of this framework at several [clients](https://qxf2.com/clients). In all cases, this framework helped us write automated tests within the first week of our engagement. We hope you find this framework useful too! 

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
	
	|__endpoints: Contains our Base Mechanize, different End Points, API Player, API Interface

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
	-S	used to post pytest reports on the Slack channel		E.g: py.test -S Y -v > log/pytest_report.log
	-n 	used to run tests in parallel					E.g: py.test -n 3 -v (This will run three tests in parallel)

b)python tests/test_example_form.py (can also be used to run standalone test) 	

c)python tests/test_example_form.py -B Chrome (to run against chrome)

d)python tests/test_api_example.py (make sure to run sample cars-api available at qxf2/cars-api repository before api test run)

--------
ISSUES?
--------

a) If Python complains about an "Import" exception, please 'pip install $module_name'

b) If you don't have drivers set up for the web browsers, you will see a helpful error from Selenium telling you where to go and get them

c) If your are using firefox 47 and above, you need to set up Geckodriver. Refer following link for setup: https://qxf2.com/blog/selenium-geckodriver-issue/

d) On Ubuntu, you may run into an issue installing the cryptography module. You need to `sudo apt-get install libssl-dev` and then run `sudo pip install -r requirements.txt`

-----------
NEED HELP?
-----------
Struggling to get your GUI automation going? You can hire Qxf2 Services to help. Contact us at mak@qxf2.com
