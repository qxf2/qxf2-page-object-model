
class Screenshot_Objects:
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

