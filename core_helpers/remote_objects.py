"""
Helper class for Remote Objects
"""

class Remote_Objects:
    def __init__(self):
        self.image_url_list = []
        self.msg_list = []
        self.testrail_flag = False
        self.tesults_flag = False
        self.browserstack_flag = False
        self.test_run_id = None

    def register_browserstack(self):
        "Register Browser Stack with Page"
        self.browserstack_flag = True
        from utils.BrowserStack_Library import BrowserStack_Library # pylint: disable=import-error,import-outside-toplevel
        self.browserstack_obj = BrowserStack_Library()

    def register_testrail(self):
        "Register TestRail with Page"
        from utils.Test_Rail import Test_Rail  # pylint: disable=import-error,import-outside-toplevel
        self.testrail_flag = True
        self.testrail_object = Test_Rail()
        self.write('Automation registered with TestRail',level='debug')

    def append_latest_image(self,screenshot_name):
        "Get image url list from Browser Stack"
        screenshot_url = self.browserstack_obj.get_latest_screenshot_url()
        image_dict = {}
        image_dict['name'] = screenshot_name
        image_dict['url'] = screenshot_url
        self.image_url_list.append(image_dict)

    def register_tesults(self):
        "Register Tesults with Page"
        self.tesults_flag = True
        from utils import Tesults # pylint: disable=import-error,import-outside-toplevel
        self.tesult_object = Tesults

    def report_to_testrail(self,case_id,test_run_id,result_flag,msg=''):
        "Update Test Rail"
        if self.testrail_flag is True:
            msg += '\n'.join(self.msg_list)
            msg = msg + "\n"
            if self.browserstack_flag is True:
                for image in self.image_url_list:
                    msg += '\n' + '[' + image['name'] + ']('+ image['url']+')'
                msg += '\n\n' + '[' + 'Watch Replay On BrowserStack' + ']('+ self.session_url+')'
            self.testrail_object.update_testrail(case_id,test_run_id,result_flag,msg=msg)
        self.image_url_list = []
        self.msg_list = []

    def set_test_run_id(self,test_run_id):
        "Set TestRail's test run id"
        self.test_run_id = test_run_id