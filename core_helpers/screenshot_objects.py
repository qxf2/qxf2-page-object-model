"""
Helper class for Screenshot Objects
"""
import os
import shutil
from .gif_maker import make_gif as gif_maker
import conf.screenshot_conf as conf

class Screenshot_Objects:
    def __init__(self):
        self.tesults_flag = False
        self.images = []

    def save_screenshot(self,screenshot_name,pre_format="      #Debug screenshot: "):
        "Take a screenshot"
        if os.path.exists(self.screenshot_dir + os.sep + screenshot_name+'.png'):
            for i in range(1,100):
                if os.path.exists(self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.png'):
                    continue
                else:
                    os.rename(self.screenshot_dir + os.sep +screenshot_name+'.png',self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.png')
                    break
        screenshot_name = self.screenshot_dir + os.sep + screenshot_name+'.png'
        self.driver.get_screenshot_as_file(screenshot_name)
        if self.rp_logger:
            self.save_screenshot_reportportal(screenshot_name)
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
            self.write("Exception when trying to get rplogger",'critical')
            self.write(str(e),'critical')
            self.exceptions.append("Error when trying to get reportportal logger")

    def make_gif(self):
        "Create a gif of all the screenshots within the screenshots directory"
        self.gif_file_name = gif_maker(self.screenshot_dir,name=self.calling_module)

        return self.gif_file_name

    def set_directory_structure(self):
        "Setup the required directory structure if it is not already present"
        try:
            self.screenshots_parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'screenshots'))
            if not os.path.exists(self.screenshots_parent_dir):
                os.makedirs(self.screenshots_parent_dir)
            self.logs_parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'log'))
            if not os.path.exists(self.logs_parent_dir):
                os.makedirs(self.logs_parent_dir)
        except Exception as e:
            # Using print as log_obj wouldnt be created to write this exception to log file
            print("Exception when trying to set screenshot directory due to error:",str(e))

    def get_test_name(self):
        "Returns the name of the test case by extracting it from the calling module."
        self.testname = self.get_calling_module()
        self.testname = self.testname.replace('<','')
        self.testname = self.testname.replace('>','')
        return self.testname

    def screenshot_directory(self, testname):
        "It checks for an existing screenshot directory, handles overwriting, and returns the path of the saved screenshot directory."
        overwrite_flag=conf.overwrite_flag
        self.screenshot_dir = self.screenshots_parent_dir + os.sep + testname
        if os.path.exists(self.screenshot_dir):
            if overwrite_flag is False:
                for i in range(1,4096):
                    if os.path.exists(self.screenshot_dir + '_'+str(i)):
                        continue
                    else:
                        os.rename(self.screenshot_dir,self.screenshot_dir +'_'+str(i))
                    break
            else:
                try:
                    shutil.rmtree(self.screenshot_dir)
                except OSError as e:
                    self.write("Error: %s - %s." % (e.filename, e.strerror),'critical')
        return self.screenshot_dir

    def create_screenshot_dir(self, screenshot_dir):
        "Create the screenshot directory if it doesn't exists already"
        try:
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            return screenshot_dir
        except Exception as e:
            self.write("Exception when trying to set screenshot directory",'critical')
            self.write(str(e),'critical')
            self.exceptions.append("Error when setting up the screenshot directory")
