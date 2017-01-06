"""
Class to wrap around parsing command line options
"""

import os, sys
import optparse

class Option_Parser:
    "The option parser class"
    
    def __init__(self,usage="\n----\n%prog -b <OPTIONAL: Browser> -c <OPTIONAL: configuration_file> -u <OPTIONAL: APP URL> -r <Test Run Id> -t <OPTIONAL: testrail_configuration_file> -s <OPTIONAL: sauce flag>\n----\nE.g.: %prog -b FF -c .conf -u http://qxf2.com -r 2 -t testrail.conf -s Y\n---"
):
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
                            default="https://qxf2.com",
                            help="The url of the application")
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
                            help="Run the test in Browserstack or Sauce: Y or N")
        self.parser.add_option("-O","--os_version",
                            dest="os_version",
                            help="The operating system: xp, 7",
                            default="7")
        self.parser.add_option("-V","--ver",
                            dest="browser_version",
                            help="The version of the browser: a whole number",
                            default=45)
        self.parser.add_option("-P","--os_name",
                            dest="os_name",
                            help="The operating system: Windows , Linux",
                            default="Windows")

        
    def add_option(self,option_letter,option_word,dest,help_text):
        "Add an option to our parser"
        self.parser.add(option_letter,
                        option_word,
                        dest,
                        help=help_text)


    def get_options(self):
        "Get the command line arguments passed into the script"
        (options,args)=self.parser.parse_args()

        return options

    
    def check_file_exists(self,file_path):
        "Check if the config file exists and is a file"
        self.conf_flag = True
        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                print '\n****'
                print 'Config file provided is not a file: '
                print file_path
                print '****'
                self.conf_flag = False
        else:
            print '\n****'
            print 'Unable to locate the provided config file: '
            print file_path
            print '****'
            self.conf_flag = False

        return self.conf_flag


    def check_options(self,options):
        "Check if the command line options are valid"
        result_flag = True
        if options.browser is not None:
            result_flag &= True
        else:
            result_flag = False
            print "Browser cannot be None. Use -B to specify a browser"
        if options.url is not None:
            result_flag &= True
        else:
            result_flag = False
            print "Url cannot be None. Use -U to specify a url"
        if options.remote_flag.lower() == 'y':
            if options.browser_version is not None:
                result_flag &= True
            else:
                result_flag = False
                print "Browser version cannot be None. Use -V to specify a browser version"
            if options.os_name is not None:
                result_flag &= True
            else:
                result_flag = False
                print "The operating system cannot be None. Use -P to specify an OS"
            if options.os_version is not None:
                result_flag &= True
            else:
                result_flag = False
                print "The OS version cannot be None. Use -O to specify an OS version"

        return  result_flag

    
    def print_usage(self):
        "Print the option parser's usage string"
        print self.parser.print_usage()
