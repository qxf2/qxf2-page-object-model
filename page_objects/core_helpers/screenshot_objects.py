"""
Helper class for Base_Page and Mobile_Base_Page consisiting of Scrreenshot objects
"""
import os
from utils import Gif_Maker
class Screenshot_Objects:
    """Class to handle screenshots"""
    def append_latest_image(self,screenshot_name):
        "Get image url list from Browser Stack"
        screenshot_url = self.browserstack_obj.get_latest_screenshot_url()
        image_dict = {}
        image_dict['name'] = screenshot_name
        image_dict['url'] = screenshot_url
        self.image_url_list.append(image_dict)

    def save_screenshot(self,screenshot_name,pre_format="      #Debug screenshot: "):
        "Take a screenshot"
        if self.browserstack_flag is True and conf.screenshot_conf.BS_ENABLE_SCREENSHOTS is False:
            return
        if os.path.exists(self.screenshot_dir + os.sep + screenshot_name+'.png'):
            for i in range(1,100):
                if os.path.exists(self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.png'):
                    continue
                else:
                    os.rename(self.screenshot_dir + os.sep +screenshot_name+'.png',self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.png')
                    break
        screenshot_name = self.screenshot_dir + os.sep + screenshot_name+'.png'
        self.driver.get_screenshot_as_file(screenshot_name)
	    #self.conditional_write(flag=True,positive= screenshot_name + '.png',negative='', pre_format=pre_format)
        if self.rp_logger:
            self.save_screenshot_reportportal(screenshot_name)
        if self.browserstack_flag is True:
            self.append_latest_image(screenshot_name)
        if self.tesults_flag is True:
            self.images.append(screenshot_name)

    def save_screenshot_reportportal(self,image_name):
        "Method to save image to ReportPortal"
        try:
            with open(image_name, "rb") as fh:
                image = fh.read()
            screenshot_name = os.path.basename(image_name)
            self.rp_logger.info(
                screenshot_name,
                attachment={
                    "name": screenshot_name,
                    "data": image,
                    "mime": "image/png"
                },
            )
        except Exception as e:
            self.write("Exception when trying to get rplogger")
            self.write(str(e))
            self.exceptions.append("Error when trying to get reportportal logger")

    def make_gif(self):
        "Create a gif of all the screenshots within the screenshots directory"
        self.gif_file_name = Gif_Maker.make_gif(self.screenshot_dir,name=self.calling_module)
        return self.gif_file_name

    def set_directory_structure(self):
        "Setup the required directory structure if it is not already present"
        try:
            self.screenshots_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','screenshots'))
            if not os.path.exists(self.screenshots_parent_dir):
                os.makedirs(self.screenshots_parent_dir)
            self.logs_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','log'))
            if not os.path.exists(self.logs_parent_dir):
                os.makedirs(self.logs_parent_dir)
        except Exception as e:
            # Using print as log_obj wouldnt be created to write this exception to log file
            print("Exception when trying to set screenshot directory due to error:",str(e))

    def get_test_name(self):
        testname = self.get_calling_module()
        testname = testname.replace('<','')
        testname = testname.replace('>','')
        return testname

    def screenshot_directory(self, testname):
        screenshot_dir = self.screenshots_parent_dir + os.sep + testname
        if os.path.exists(screenshot_dir) and overwrite_flag is True:
            for i in range(1,4096):
                if os.path.exists(screenshot_dir + '_'+str(i)):
                    continue
                else:
                    os.rename(screenshot_dir,screenshot_dir +'_'+str(i))
                    break

        return screenshot_dir







