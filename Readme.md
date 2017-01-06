--------
Welcome
--------
This repository contains Qxf2 Services's test automation framework. You can use this to write your Selenium and Appium tests. We love Python - so this framework is written completely in Python. Our framework is based on the Page Object pattern - a design pattern that makes maintaining and developing robust tests easy. 



---------
1. SETUP
---------
a) Install Python 2.x
b) 'pip install selenium' -installs selenium 
c) Add both to your PATH environment variable
d) If you do not have it already, get pip install
e) 'pip install requests' -installs requests module
f) 'pip install Appium-Python-Client' -installs Appium-Python-Client
g) 'pip install pytest' -installs pytest: test runner
h) 'pip install pytest-xdist' -installs pytest x-dist module to run tests in parallel
i) 'pip install mechanize' -installs mechanize module
j) Update 'browserstack.credentials' if you want to run on BrowserStack
k) In case you have TestRail Integration update the testrail.conf with proper case ids. Also update the testrail.env with url,user,password.

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
	|__utils: All utility modules (email_util,TestRail, BrowserStack, Base Logger) are kept in this folder
	
---------------------------
COMMANDS FOR RUNNING TESTS
---------------------------

a)py.test [options]

	-s	used to display the output on the screen			E.g: py.test -s (This will run all the tests in the directory and subdirectories)
	-U  	used to run against specific URL				E.g: py.test -U http://YOUR_localhost_URL (This will run against your local instance)
	-M  	used to run tests on Browserstack/Sauce Lab		E.g: py.test -s -M Y -U https://qxf2.com	
	-B all	used to run the test against multiple browser 			E.g: py.test -B all(This will run each test against the list of browsers specified in the conftest.py file,firefox and chrome in our case)
	-V/-O	used to run against different browser versions/os versions	E.g: py.test -V 44 -O 8 (This will run each test 4 times in different browser version(default=45 & 44) and OS(default=7 & 8) combination)
	-h	help for more options 						E.g: py.test -h
	-k      used to run tests which match the given substring expresion 	E.g: py.test -k table  (This will trigger test_example_table.py test)
	
b)python tests/test_example_form.py (can also be used to run standalone test) 	
	
--------
ISSUES?
--------

a) If Python complains about an Import exception, please 'pip install $module_name'
b) If you are not setup with the drivers for the web browsers, you will see a helpful error from Selenium telling you where to go and get them
c) If your are using firefox 47 and above, you need to setup with Geckodriver. Refer following link for setup: https://qxf2.com/blog/selenium-geckodriver-issue/

-----------
NEED HELP?
-----------
Are you struggling to get your GUI automation going? You can hire Qxf2 Services to help. Contact us at mak@qxf2.com