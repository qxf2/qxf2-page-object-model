"""
Implementing the questionaty library to fetch the users choices for different arguments
"""
import questionary
import os
import sys
from conf import api_example_conf
from clear_screen import clear


def set_default_flag_gui(base_url,browser,browser_version,os_version,os_name,remote_flag,testrail_flag,tesults_flag,test_run_id,remote_project_name,remote_build_name):
    "This checks if the user wants to run the test with the default options or no"

    questionary.print("\nDefault Options",style="bold fg:green")
    questionary.print("**********",style="bold fg:green")
    print("Browser:",browser)
    print("OS name:",os_name)
    print("OS version:",os_version)
    print("Remote Flag status:",remote_flag)
    print("Testrail Flag status:",testrail_flag)
    print("Tesults Flag status",tesults_flag)
    questionary.print("**********",style="bold fg:green")

    default=questionary.select("Do you want to run the test with the default set of options?",choices=["Yes","No"]).ask() #ask if the user wants to run the test with default options
    if default=="Yes":
        default_flag=True
    else:
        default_flag=False

    return default_flag

def ask_questions_gui(base_url,browser,browser_version,os_version,os_name,remote_flag,testrail_flag,tesults_flag,test_run_id,remote_project_name,remote_build_name):
    "This module asks the users questions on what options they wish to run the test with and stores their choices"
    clear()
    while True:
        questionary.print("\nUse up and down arrow keys to switch between options.\nUse Enter key to select an option",style="bold fg:yellow")
        questionary.print("\nSelected Options",style="bold fg:green")
        questionary.print("**********",style="bold fg:green")
        print("Browser selected:",browser)
        if browser_version==[]:
            print("Browser version selected: None")
        else:
            print("Browser version selected:",browser_version)
        if os_name==[]:
            print("OS selected: None")
        else:
            print("OS selected:",os_name)
        if os_version==[]:
            print("OS version selected: None")
        else:
            print("OS version selected:",os_version)
        print("Remote flag status:",remote_flag)
        print("Testrail flag status:",testrail_flag)
        print("Tesults flag status",tesults_flag)
        questionary.print("**********",style="bold fg:green")


        response = questionary.select("What would you like to change?",choices=["Browser","Browser Version","Os Version","Os Name","Remote flag status","Testrail flag status","Tesults flag status","Set Remote credentials","Revert back to default options","Run","Exit"]).ask()

        clear()
        if response=="Browser":
            browser=questionary.select("Select the browser",choices=["chrome","firefox","safari"]).ask()

            if remote_flag=="Y":
                browser_version= []
                questionary.print("Please select the browser version",style="bold fg:darkred")

        if response=="Browser Version":
            if browser=="chrome":
                browser_version=questionary.select("Select the browser version",choices=["64","65"]).ask()

            elif browser=="firefox":
                browser_version=questionary.select("Select the browser version",choices=["57","58"]).ask()

            elif browser=="safari":
                browser_version=questionary.select("Select the browser version",choices=["8"]).ask()


        if response=="Remote flag status":
            remote_flag=questionary.select("Do you want to run the test remotely?",choices=["Yes","No"]).ask()

            if remote_flag=="Yes":
                remote_flag="Y"
                browser="chrome"
                os_name="Windows"
                os_version="10"
                browser_version="65"
                questionary.print("The default remote test options has been selected",style="bold fg:green")
            else:
                remote_flag="N"

        if response=="Os Version":

            if os_name=="Windows":
                os_version=questionary.select("Select the OS version",choices=["7","xp","10"]).ask()
            elif os_name=="OS X":
                os_version=questionary.select("Select the OS version",choices=["yosemite"]).ask()
            else:

                questionary.print("Please select the OS Name first",style="bold fg:darkred")

        if response=="Os Name":
            os_name=questionary.select("Enter the OS version",choices=["Windows","OS X"]).ask()

            if remote_flag=="Y":
                os_version=[]
                questionary.print("Please select the OS Version",style="bold fg:darkred")

        if response=="Testrail flag status":
            testrail_flag=questionary.select("Enter the testrail flag",choices=["Yes","No"]).ask()

            if testrail_flag=="Yes":
                testrail_flag="Y"
            else:
                testrail_flag="N"
        if response=="Tesults flag status":
            tesults_flag=questionary.select("Enter the tesults flag",choices=["Yes","No"]).ask()

            if tesults_flag=="Yes":
                tesults_flag="Y"
            else:
                tesults_flag="N"

        if response=="Set Remote credentials":
            platform = questionary.select("Select the remote platform on which you wish to run the test on",choices=["Browserstack","Saucelabs"]).ask()
            if platform=="Browserstack":
                platform="BS"
            else:
                platform="SL"
            username = questionary.text("Enter the Username").ask()
            password = questionary.password("Enter the password").ask()
            with open("conf/remote_credentials.py",'w') as f:
                f.write("REMOTE_BROWSER_PLATFORM = '%s' \nUSERNAME = '%s' \nACCESS_KEY = '%s'"%(platform,username,password))
            questionary.print("Updated the credentials successfully",style="bold fg:green")

        if response=="Revert back to default options":
                browser="chrome"
                os_name=[]
                os_version=[]
                browser_version=[]
                remote_flag="N"
                testrail_flag="N"
                tesults_flag="N"
                questionary.print("Reverted back to the default options",style="bold fg:green")

        if response=="Run":

            if remote_flag=="Y":
                if browser_version==[]:
                    questionary.print("Please select the browser version before you run the test",style="bold fg:darkred")

                elif os_version==[]:
                    questionary.print("Please select the OS version before you run the test",style="bold fg:darkred")
                else:
                    break
            else:
                break

        if response=="Exit":
            sys.exit()

    return browser,browser_version,remote_flag,os_name,os_version,testrail_flag,tesults_flag



def ask_questions_mobile(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, test_run_id,app_name,app_path):
    "This module asks the users questions on what options they wish to run the test with and stores their choices"

    clear()
    while True:
        questionary.print("\nUse up and down arrow keys to switch between options.\nUse Enter key to select an option",style="bold fg:yellow")
        questionary.print("\nSelected Options",style="bold fg:green")
        questionary.print("**********",style="bold fg:green")
        print("Mobile OS Name:",mobile_os_name)
        print("Mobile OS Version:",mobile_os_version)
        print("Device Name:",device_name)
        print("App Package:",app_package)
        print("App Activity:",app_activity)
        print("Remote Flag status:",remote_flag)
        print("Device Flag status:",device_flag)
        print("Testrail Flag status:",testrail_flag)
        print("Tesults Flag status:",tesults_flag)
        print("App Name:",app_name)
        print("App Path:",app_path)
        print("Appium Version:",app_activity)
        questionary.print("**********",style="bold fg:green")


        response = questionary.select("What would you like to change?",choices=["Mobile OS Name","Mobile OS Version","Device Name","App Package","App Activity","Remote Flag status","Testrail flag status","Tesults flag status","App Name","App Path","Revert back to default options","Run","Exit"]).ask()

        clear()

        if response=="Mobile OS Name":
            mobile_os_name=questionary.select("Select the Mobile OS",choices=["Android","iOS"]).ask()

        if response=="Mobile OS Version":
            mobile_os_version=questionary.select("Select the Mobile OS version",choices=["6.0","7.0","7.1","8.0","8.1","9.0", "Other versions"]).ask()

        if response=="Device Name":

            print("The devices that support Android",mobile_os_version,"has been listed. Please select any one device")
            if mobile_os_version=="10.0":
                device_name=questionary.select("Select the device name",choices=["Samsung Galaxy S20","Samsung Galaxy Note 20", "Google Pixel 4", "Google Pixel 3","OnePlus 8","Other Devices"]).ask()
                if device_name=="Other Devices":
                    questionary.text("Enter the device name").ask()

            if mobile_os_version=="9.0":
                device_name=questionary.select("Select the device name",choices=["Samsung Galaxy S10","Samsung Galaxy A51", "Google Pixel 3a", "Xiaomi Redmi Note 8","OnePlus 7","Other Devices"]).ask()
                if device_name=="Other Devices":
                    questionary.text("Enter the device name").ask()

            if mobile_os_version=="8.0":
                device_name=questionary.select("Select the device name",choices=["Samsung Galaxy S9","Google Pixel 2","Other Devices"]).ask()
                if device_name=="Other Devices":
                    questionary.text("Enter the device name").ask()

            if mobile_os_version=="8.1":
                device_name=questionary.select("Select the device name",choices=["Samsung Galaxy Note 9","Other Devices"]).ask()
                if device_name=="Other Devices":
                    questionary.text("Enter the device name").ask()

            if mobile_os_version=="7.1":
                device_name=questionary.select("Select the device name",choices=["Samsung Galaxy Note 8","Google Pixel","Other Devices"]).ask()
                if device_name=="Other Devices":
                    questionary.text("Enter the device name").ask()

            if mobile_os_version=="7.0":
                device_name=questionary.select("Select the device name",choices=["Samsung Galaxy S8","Google Nexus 6P","Other Devices"]).ask()
                if device_name=="Other Devices":
                    questionary.text("Enter the device name").ask()

            if mobile_os_version=="6.0":
                device_name=questionary.select("Select the device name",choices=["Samsung Galaxy S7","Google Nexus 6","Other Devices"]).ask()
                if device_name=="Other Devices":
                    questionary.text("Enter the device name").ask()

            if mobile_os_version=="Other versions":
                questionary.text("Enter the Device name").ask()

        if response=="App Package":
            app_package=questionary.text("Enter the app package name").ask()

        if response=="App Activity":
            app_package=questionary.text("Enter the App Activity").ask()

        if response=="Remote Flag status":
            remote_flag=questionary.select("Select the remote flag status",choices=["Yes","No"]).ask()
            if remote_flag=="Yes":
                remote_flag="Y"
            else:
                remote_flag="N"

        if response=="Testrail Flag status":
            testrail_flag=questionary.select("Select the testrail flag status",choices=["Yes","No"]).ask()
            if testrail_flag=="Yes":
                testrail_flag="Y"
            else:
                testrail_flag="N"

        if response=="Tesults Flag status":
            tesults_flag=questionary.select("Select the tesults flag status",choices=["Yes","No"]).ask()
            if tesults_flag=="Yes":
                tesults_flag="Y"
            else:
                tesults_flag="N"

        if response=="App Name":
            app_name=questionary.text("Enter App Name").ask()

        if response=="App Path":
            app_path=questionary.path("Enter the path to your app").ask()

        if response=="Revert back to default options":
                mobile_os_name ="Android"
                mobile_os_version="8.0"
                device_name="Samsung Galaxy S9"
                app_package="com.dudam.rohan.bitcoininfo"
                app_activity=".MainActivity"
                remote_flag="N"
                device_flag="N"
                testrail_flag="N"
                tesults_flag="N"
                app_name="Bitcoin Info_com.dudam.rohan.bitcoininfo.apk"
                app_path=None


        if response=="Run":
            if app_path == None:
                questionary.print("Please enter the app path before you run the test",style="bold fg:darkred")
            else:
                break



        if response=="Exit":
            sys.exit()


    return mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, test_run_id,app_name,app_path

def ask_questions_api(api_url,session_flag=True):
    clear()
    while True:

        questionary.print("\nSeleted Options",style="bold fg:green")
        questionary.print("**********",style="bold fg:green")
        print("API URL:",api_url)
        print("Session flag status:",session_flag)
        questionary.print("**********",style="bold fg:green")

        response=questionary.select("What would you like to change", choices=["API URL","Session flag status","Reset back to default settings","Run","Exit"]).ask()

        clear()
        if response=="Session flag status":
            session_flag=questionary.select("Select the Session flag status",choices=["True","False"]).ask()
            if session_flag =="True":
                session_flag=True
            if session_flag =="False":
                session_flag=False

        if response=="API URL":
            api_url=questionary.select("Select the API url",choices=["localhost","http://35.167.62.251/","Enter the URL manually"]).ask()
            if api_url=="localhost":
                api_url=api_example_conf.api_url
            if api_url=="Enter the URL manually":
                api_url= questionary.text("Enter the url").ask()


        if response =="Reset back to default settings":
            api_url= api_example_conf.api_url
            session_flag=True
            questionary.print("Reverted back to default settings",style="bold fg:green")

        if response=="Run":
            break

        if response=="Exit":
            sys.exit()

    return api_url,str(session_flag)




"""
remote_flag=questionary.select("Do you want to run the test remotely?",choices=["Yes","No"]).ask()
if remote_flag=="Yes":
    remote_flag="Y"
else:
    remote_flag="N"

browser=questionary.select("Enter the browser",choices=["chrome","firefox"]).ask()


base_url= "https://qxf2.com/"
browser = "chrome"
browser_version = []
os_version= []
os_name=[]
remote_flag="N"
testrail_flag="N"
tesults_flag="N"
test_run_id=None
remote_project_name=None
remote_build_name=None
#testname=test_example_form
#questionary_flag= "n"
"""