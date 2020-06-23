"""
Class to wrap around parsing command line options
"""
import optparse
from conf import base_url_conf as conf


class Option_Parser:
    "The option parser class"

    def __init__(self,usage="\n----\n%prog -b <OPTIONAL: Browser> -c <OPTIONAL: configuration_file> -u <OPTIONAL: APP URL> -a <OPTIONAL: API URL> -r <Test Run Id> -t <OPTIONAL: testrail_configuration_file> -s <OPTIONAL: sauce flag>\n----\nE.g.: %prog -b FF -c .conf -u http://qxf2.com -r 2 -t testrail.conf -s Y\n---"):
        "Class initializer"
        self.usage=usage
        self.parser=optparse.OptionParser()
        self.set_standard_options()

    def set_standard_options(self):
        "Set options shared by all tests over here"
        self.parser.add_option("-B","--browser",
                            dest="browser",
                            default="firefox",
                            help="Browser. Valid options are firefox, ie and chrome")
        self.parser.add_option("-U","--app_url",
                            dest="url",
                            default=conf.base_url,
                            help="The url of the application")
        self.parser.add_option("-A","--api_url",
                            dest="api_url",
                            default="http://35.167.62.251/",
                            help="The url of the api")
        self.parser.add_option("-X","--testrail_flag",
                            dest="testrail_flag",
                            default='N',
                            help="Y or N. 'Y' if you want to report to TestRail")
        self.parser.add_option("-R","--test_run_id",
                            dest="test_run_id",
                            default=None,
                            help="The test run id in TestRail")
        self.parser.add_option("-M","--remote_flag",
                            dest="remote_flag",
                            default="N",
                            help="Run the test in remote flag: Y or N")
        self.parser.add_option("-O","--os_version",
                            dest="os_version",
                            help="The operating system: xp, 7",
                            default="7")
        self.parser.add_option("--ver",
                            dest="browser_version",
                            help="The version of the browser: a whole number",
                            default=45)
        self.parser.add_option("-P","--os_name",
                            dest="os_name",
                            help="The operating system: Windows , Linux",
                            default="Windows")
        self.parser.add_option("-G","--mobile_os_name",
                            dest="mobile_os_name",
                            help="Enter operating system of mobile. Ex: Android, iOS",
                            default="Android")
        self.parser.add_option("-H","--mobile_os_version",
                            dest="mobile_os_version",
                            help="Enter version of operating system of mobile: 8.1.0",
                            default="6.0")
        self.parser.add_option("-I","--device_name",
                            dest="device_name",
                            help="Enter device name. Ex: Emulator, physical device name",
                            default="Google Nexus 6")
        self.parser.add_option("-J","--app_package",
                            dest="app_package",
                            help="Enter name of app package. Ex: bitcoininfo",
                            default="com.dudam.rohan.bitcoininfo")
        self.parser.add_option("-K","--app_activity",
                            dest="app_activity",
                            help="Enter name of app activity. Ex: .MainActivity",
                            default=".MainActivity")
        self.parser.add_option("-Q","--device_flag",
                            dest="device_flag",
                            help="Enter Y or N. 'Y' if you want to run the test on device. 'N' if you want to run the test on emulator.",
                            default="N")
        self.parser.add_option("-D","--app_name",
                            dest="app_name",
                            help="Enter application name to be uploaded.Ex:Bitcoin Info_com.dudam.rohan.bitcoininfo.apk.",
                            default="Bitcoin Info_com.dudam.rohan.bitcoininfo.apk")
        self.parser.add_option("-T","--tesults_flag",
                            dest="tesults_flag",
                            help="Enter Y or N. 'Y' if you want to report results with Tesults",
                            default="N")
        self.parser.add_option("--ud_id",
                      dest="ud_id",
                      help="Enter your iOS device UDID which is required to run appium test in iOS device",
                      default=None)
        self.parser.add_option("--org_id",
                        dest="org_id",
                        help="Enter your iOS Team ID which is required to run appium test in iOS device",
                        default=None)
        self.parser.add_option("--signing_id",
                        dest="signing_id",
                        help="Enter your iOS app signing id which is required to run appium test in iOS device",
                        default="iPhone Developer")
        self.parser.add_option("--no_reset_flag",
                        dest="no_reset_flag",
                        help="Pass false if you want to reset app eveytime you run app else false",
                        default="true")
        self.parser.add_option("-N","--app_path",
                            dest="app_path",
                            help="Enter app path")
        self.parser.add_option("--remote_project_name",
                            dest="remote_project_name",
                            help="The project name if its run in BrowserStack",
                            default=None)
        self.parser.add_option("--remote_build_name",
                            dest="remote_build_name",
                            help="The build name if its run in BrowserStack",
                            default=None)        
        self.parser.add_option("--appium_version",
                            dest="appium_version",
                            help="The appium version if its run in Browserstack",
                            default="1.17.0")

    def add_option(self,option_letter,option_word,dest,help_text):
        "Add an option to our parser"
        self.parser.add(option_letter,
                        option_word,
                        dest,
                        help=help_text)


    def get_options(self):
        "Get the command line arguments passed into the script"
        options=self.parser.parse_args()

        return options


    def check_file_exists(self,file_path):
        "Check if the config file exists and is a file"
        self.conf_flag = True
        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                print('\n****')
                print('Config file provided is not a file: ')
                print(file_path)
                print('****')
                self.conf_flag = False
        else:
            print('\n****')
            print('Unable to locate the provided config file: ')
            print(file_path)
            print('****')
            self.conf_flag = False

        return self.conf_flag


    def check_options(self,options):
        "Check if the command line options are valid"
        result_flag = True
        if options.browser is not None:
            result_flag &= True
        else:
            result_flag = False
            print("Browser cannot be None. Use -B to specify a browser")
        if options.url is not None:
            result_flag &= True
        else:
            result_flag = False
            print("Url cannot be None. Use -U to specify a url")
        if options.api_url is not None:
            result_flag &= True
        else:
            result_flag = False
            print("API URL cannot be None. Use -A to specify a api url")
        if options.remote_flag.lower() == 'y':
            if options.browser_version is not None:
                result_flag &= True
            else:
                result_flag = False
                print("Browser version cannot be None. Use --ver to specify a browser version")
            if options.os_name is not None:
                result_flag &= True
            else:
                result_flag = False
                print("The operating system cannot be None. Use -P to specify an OS")
            if options.os_version is not None:
                result_flag &= True
            else:
                result_flag = False
                print("The OS version cannot be None. Use -O to specify an OS version")

        # Options for appium mobile tests.
        if options.mobile_os_name is not None:
            result_flag &= True
        else:
            result_flag = False
            print("The mobile operating system cannot be None. Use -G to specify an OS.")

        if options.mobile_os_version is not None:
            result_flag &= True
        else:
            result_flag = False
            print("The mobile operating system version cannot be None. Use -H to specify an OS version.")

        if options.device_name is not None:
            result_flag &= True
        else:
            result_flag = False
            print("The device name cannot be None. Use -I to specify device name.")

        if options.app_package is not None:
            result_flag &= True
        else:
            result_flag = False
            print("The application package name cannot be None. Use -J to specify application package name.")

        if options.app_activity is not None:
            result_flag &= True
        else:
            result_flag = False
            print("The application activity name cannot be None. Use -K to specify application activity name.")

        if options.device_flag.lower() == 'n':
            result_flag &= True
        else:
            result_flag = False
            print("The device flag cannot be None. Use -Q to specify device flag.")

        return  result_flag


    def print_usage(self):
        "Print the option parser's usage string"
        print(self.parser.print_usage())
