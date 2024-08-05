![Python version](https://img.shields.io/badge/python-3.x-green?color=brightgreen)
![GitHub](https://img.shields.io/github/license/qxf2/qxf2-page-object-model?color=brightgreen)
![Maintenance](https://img.shields.io/maintenance/yes/2024?color=brightgreen)
[![CircleCI](https://circleci.com/gh/qxf2/qxf2-page-object-model.svg?style=shield)](https://circleci.com/gh/qxf2/qxf2-page-object-model)
[![BrowserStack Status](https://automate.browserstack.com/badge.svg?badge_key=cVVDdmxnTmpNL3FEeS9FUWY2S2M2Q0xLRFJoTFhVV0RUNlJRS292Sm9WWT0tLWxuS2dGeWhmK0M3SUt2d1hOR0F2TXc9PQ==--f6f4c1765a8d4d5250966b5ee1397a93da38a7a3)](https://automate.browserstack.com/public-build/cVVDdmxnTmpNL3FEeS9FUWY2S2M2Q0xLRFJoTFhVV0RUNlJRS292Sm9WWT0tLWxuS2dGeWhmK0M3SUt2d1hOR0F2TXc9PQ==--f6f4c1765a8d4d5250966b5ee1397a93da38a7a3)
![GitHub stars](https://img.shields.io/github/stars/qxf2/qxf2-page-object-model)
![GitHub forks](https://img.shields.io/github/forks/qxf2/qxf2-page-object-model)
![GitHub repo size](https://img.shields.io/github/repo-size/qxf2/qxf2-page-object-model)
![GitHub last commit](https://img.shields.io/github/last-commit/qxf2/qxf2-page-object-model)
![Codacy Badge](https://app.codacy.com/project/badge/Grade/c330930eaad64b9cabb62fee2a84fe69)

--------
A Pythonic Selenium, Appium and API test automation framework
--------
You can use this test automation framework to write

1. __Selenium__ and Python automation scripts to test web applications

2. __Appium__ and Python scripts for __mobile automation__ (Android and iOS)

3. __API automation__ scripts to test endpoints of your web/mobile applications

&nbsp;

![Qxf2 automation framework](https://qxf2.com/assets/img/framework_introduction.png)

&nbsp;

This GUI and API test automation framework is developed and maintained by [Qxf2 Services](https://qxf2.com). This framework is written in __Python__ and is based on the __Page Object Model__ - a design pattern that makes it easy to maintain and develop robust tests. We have also included our __API test automation framework__ based on the player-interface pattern in this repository. You can now write your API tests along with your Selenium and Appium tests.

We've implemented some version of this framework at several [clients](https://qxf2.com/clients). In all cases, this framework helped us write automated tests within the first week of our engagement. We hope you find this framework useful too!

Looking for ways to automate your __UI__ and __API__ tests quickly and effectively? You've come to the right place. By harnessing __AI__ and __code auto-generation__ capabilities, we've developed solutions that significantly decrease the time needed to create a fully functional test suite. For further information, please refer to the following links.
* [Qxf2's Gen AI test automation service](https://qxf2.com/qait)
* [Qxf2's API test automation service](https://qxf2.com/api-tests-autogenerate.html)

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

e)configure environmental variables 

Templates for.env files are provided.
Kindly fill in the credentials and rename the files according to the specified format.

* env_conf to .env 
	Tesults, TestRail, Gmail , Report portal and Slack credentials details can be entered here.
* env_ssh_conf to .env.ssh
    ssh server credentials used by the SSHKeywords keyword to connect to remote servers.
* env_remote to .env.remote 
    Remote WebDriver Server Details (BrowserStack/SauceLabs).

If you ran into some problems on step (d), please report them as an issue or email Arun(mak@qxf2.com).


__2. Setup for GUI/Selenium automation__


a) Get setup with your browser driver. If you don't know how to, please try:

   > [For Chrome](https://googlechromelabs.github.io/chrome-for-testing/)

   > [For Firefox](https://github.com/mozilla/geckodriver/releases)

#Note: Check Firefox version & Selenium version compatibility before downloading geckodriver.

__If your setup goes well__, you should be to run a simple test with this command:

1. Chrome: `python -m pytest -k example_form --browser Chrome`

2. Firefox: `python -m pytest -k example_form --browser Firefox`

__Optional steps__ for integrating with third-party tools:

* [Integrate our Python test automation framework with Testrail](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-TestRail-using-Python)
* [Integration with ReportPortal](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-ReportPortal) 
* [Integrate our Python GUI/web automation framework with BrowserStack ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Cloud-Services#browserstack)
* [Integrate our Python Selenium automation framework with Sauce Labs ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Cloud-Services#sauce-labs)
* [Integrate our Python GUI/web automation framework with LambdaTest](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Cloud-Services#lambdatest)
* [Run Python integration tests on Jenkins ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-CI-Tools#jenkins)
* [Run Python integration tests on CircleCI ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-CI-Tools#circleci)
* [Post Python automation test results on Slack ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Slack)
* [Email pytest report with Gmail](https://github.com/qxf2/qxf2-page-object-model/wiki/Email-pytest-report-with-Gmail)


__3. Setup for Mobile/Appium automation__


a) [Install appium globally using npm](https://appium.io/docs/en/latest/quickstart/install/)

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
Directory structure of our current Templates
```
   ./

   |_ conf: For all configurations files
   
   |_ core_helpers: Contains our web app and mobile app helpers and DriverFactory  

   |_ endpoints: Contains our Base Mechanize, different End Points, API Player, API Interface

   |_ integrations: Contains cross-browsers, reporting tools and reporting channel integrations (BrowserStack, SauceLabs, Lambdatest, TestRail, Tesults, Slack, Gmail) 

   |_ log: Log files for all tests

   |_ page_objects: Contains our PageFactory, different Page Objects examples

   |_ screenshots: For screenshots

   |_ tests: Put your tests here

   |_ utils: All utility modules (ssh_util, compare csv, compare images, Base Logger, etc) are kept in this folder

   |_ conftest.py: Configuration file to add different fixtures used in py.test

   |_ .env and .env.remote: For credential details. Refer env_conf and env_remote file and rename it to .env and .env_conf. 
```
---------------------------
COMMANDS FOR RUNNING TESTS
---------------------------


### a) General Command
`python -m pytest [options]`

### Options

- **`--app_url`**  
  *Runs against a specific URL.*  
  **Example:**  
  `python -m pytest --app_url http://YOUR_localhost_URL`  
  This will run against your local instance.

- **`--remote_flag`**  
  *Runs tests on Browserstack/LambdaTest/Sauce Labs.*  
  **Example:**  
  `python -m pytest -s --remote_flag Y --app_url https://qxf2.com`

- **`--browser all`**  
  *Runs the tests against multiple browsers.*  
  **Example:**  
  `python -m pytest --browser all`  
  This will run each test against the list of browsers specified in the `conf/browser_os_name_conf.py` file (e.g., Firefox and Chrome).

- **`--ver / --os_name / --os_version`**  
  *Runs against different browser versions/OS and OS versions.*  
  **Example:**  
  `python -m pytest --ver 120 --os_name windows --os_version 11 --remote_flag y`  
  This will run each test with defalut browser (chrome) and provided combination (browser version 120 windows 11)

- **`-h`**  
  *Displays help for more options.*  
  **Example:**  
  `python -m pytest -h`

- **`-k`**  
  *Runs tests matching the given substring expression.*  
  **Example:**  
  `python -m pytest -k table`  
  This will trigger tests that match the pattern, such as `test_example_table.py`.

- **`--slack_flag`**  
  *Posts pytest reports on the Slack channel.*  
  **Example:**  
  `python -m pytest --slack_flag Y -v > log/pytest_report.log`
  This will send the pytest-report on configued slack channel at the end of test run.

- **`-n`**  
  *Runs tests in parallel.*  
  **Example:**  
  `python -m pytest -n 3 -v`  
  This will run three tests in parallel.

- **`--tesults`**  
  *Reports test results to Tesults.*  
  **Example:**  
  `python -m pytest tests/test_example_form.py --tesults Y`

- **`--interactive_mode_flag`**  
  *Runs the tests interactively.*  
  **Example:**  
  `python -m pytest tests/test_example_form.py --interactive_mode_flag Y`  
  This option allows the user to pick the desired configuration to run the test from a menu displayed.

  **Note:** If you wish to run the test in interactive mode on Git Bash for Windows, set your bash alias by adding the following command to `.bashrc`:  
  `alias python='winpty python.exe'`

- **`--summary`**  
  *Summarizes the pytest results in an HTML report.*  
  **Example:**  
  `python -m pytest -k example_table --summary y`  
  **Note:** You need to provide your `OPENAI_API_KEY` using `export OPENAI_API_KEY=<your-key>`.

### b) Specific Commands

- **Standalone Test**  
	`python -m pytest tests/test_example_form.py`

- **Run Against Specific Browser**  
	`python -m pytest tests/test_example_form.py --browser Chrome`

- **API Test**  
	`python -m pytest tests/test_api_example.py`  
	**Note:** Ensure the sample `cars-api` is available at `qxf2/cars-api` repository before running the API test.

- **Mobile Test Run on Browserstack/Sauce Labs**  
	`python -m pytest tests/test_mobile_bitcoin_price --mobile_os_version <android version> --device_name <simulator> --app_path <.apk location on local> --remote_flag Y`  
	**Note:** For running tests on Browserstack/Sauce Labs, update the Browser_Plaform, Username and AccessKey in `.env.remote` from your Browserstack/Sauce Labs account. Refer our wiki page for more details: [Integrate our Python Selenium automation framework with Cloud Services ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Cloud-Services)

- **Run Test along with Tesults**  
	`python -m pytest tests/test_example_form.py --tesults Y`  
	**Note:** For running the test along with Tesults, update the .env file with target_token and run the above command. Refer env_conf file for configuration.
		
- **Run Tests along with ReportPortal**  
	`python -m pytest -k example --reportportal`  
	**Note:** For running the test along with ReportPortal, update the .env file with report portal credential details and run the above command. Refer our wiki page for more details: [Integration with ReportPortal](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-ReportPortal) 

- **Run Tests along with TestRail**  
	`python -m pytest -k example --testrail_flag Y`  
	**Note:** For running the test along with TestRail, update the .env file with TestRails credential details and run the above command. Refer our wiki page for more details: [Integrate our Python test automation framework with Testrail](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-TestRail-using-Python)

- **Post test results on Slack**  
	`pytest -k example_form --slack_flag y -v > log/pytest_report.log`  
	**Note:** For setup and other details, refer our wiki page: [Post Python automation test results on Slack ](https://github.com/qxf2/qxf2-page-object-model/wiki/Integration-with-Slack)  

- **Email pytest report with Gmail**  
	`pytest -s -v --email_pytest_report y --html=log/pytest_report.html`  
	**Note:** For setup and other details, refer our wiki page: [Email pytest report with Gmail](https://github.com/qxf2/qxf2-page-object-model/wiki/Email-pytest-report-with-Gmail)


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
