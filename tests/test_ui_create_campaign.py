"""
This is an example automated test to help you learn Qxf2's framework
Our automated test will do the following:
    #Open Qxf2 selenium-tutorial-main page.
    #Fill the example form.
    #Click on Click me! button and check if its working fine.
"""
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.example_form_conf as conf
import conf.testrail_caseid_conf as testrail_file
import pytest


@pytest.mark.GUI
def test_ui_create_campaign(test_obj):

    "Run the test"
    #try:
    if True:
        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object and fill the example form.
        test_obj = PageFactory.get_page_object("Main Page")
        #Set start_time with current time
        start_time = int(time.time())


        # Turn on the highlighting feature
        test_obj.turn_on_highlight()
        

        #Verify the page title in newsletter generator
        page_title = test_obj.verify_page_title()
        result_flag = False
        if page_title == 'Qxf2 Newsletter Generator':
            result_flag = True
        test_obj.log_result(result_flag,
                        positive="Succesfully found the title",
                        negative="Failed to find the title")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))

        #Verify and hover the menu in home page
        hamburger_menu = test_obj.hover_menu()

        #Verify and click the add article in menu
        options = "Add Article"
        click_add_article = test_obj.click_menu_content(options)
        test_obj.log_result(click_add_article,
        positive="The %s is clicked"%options,
        negative="The %s is not clicked"%options)

        #Add article
        result_flag = test_obj.add_article()
        test_obj.log_result(result_flag,
        positive="The URL is set",
        negative="The %URL is not set")   

        #Add title
        title = "This is a automated title for UI test"

        result_title = test_obj.add_title(title)
        test_obj.log_result(result_title,
        positive="The title is set to:"+title,
        negative="The title is not set")

        #Add description
        description = "This is a manual set description for UI automation"

        result_description = test_obj.add_description(description)
        test_obj.log_result(result_description,
        positive="The description is set to:"+description,
        negative="The description is not set")

        #Add Time
        result_time = test_obj.add_time()
        test_obj.log_result(result_time,
        positive="The time is set",
        negative="The time is not set")

        #Click category
        article_category = "comic"
        result_click_category = test_obj.click_category(article_category)
        test_obj.log_result(result_click_category,
        positive="The category is clicked",
        negative="The category is not clicked")

        #Click Add article button
        result_add_article_button = test_obj.click_add_article_button()
        test_obj.log_result(result_add_article_button,
        positive="The add article button is clicked and the record is added",
        negative="The add article button is not clicked and the record is not added") 

        #Verify and hover the menu in home page
        hamburger_menu = test_obj.hover_menu()         

        #Verify and click the add article in menu
        options = "Create Newsletter"
        click_add_article = test_obj.click_menu_content(options)
        test_obj.log_result(click_add_article,
        positive="The %s is clicked"%options,
        negative="The %s is not clicked"%options)    

        #Create newsletter
        article_category = "comic"
        subject = "99-Dec-1900"
        opener = "From the simplest to the most complex application, automation is present in many forms in our everyday life. Common examples include household thermostats controlling boilers, the earliest automatic telephone switchboards, electronic navigation systems, or the most advanced algorithms behind self-driving cars."
        preview = "From the simplest to the most complex application, automation is present in many forms in our everyday life. Common examples include household"
        url_option = "This is a automated title for UI test"

        result_create_newsletter = test_obj.create_newsletter(article_category,subject,opener,preview,url_option)
        test_obj.log_result(result_create_newsletter,
        positive="The create newsletter is created successfully",
        negative="The create newsletter is not created successfully")        

        #Check preview newsletter content

        result_check_preview_content = test_obj.check_preview_content(opener)
        test_obj.log_result(result_check_preview_content,
        positive="The preview newsletter content is created successfully",
        negative="The preview newsletter content is not created successfully") 

        #create campaign

        result_create_campaign = test_obj.create_campaign()      
        test_obj.log_result(result_create_campaign,
        positive="Campaign is succesfully created",
        negative="Campaign is not created")       


    #except Exception as e:
    #    print("Exception when trying to run test: %s"%__file__)
    #    print("Python says:%s"%str(e))

    assert expected_pass == actual_pass, "Test failed: %s"%__file__


#---START OF SCRIPT
if __name__=='__main__':
    print("Start of %s"%__file__)
    #Creating an instance of the class
    options_obj = Option_Parser()
    options = options_obj.get_options()

    #Run the test only if the options provided are valid
    if options_obj.check_options(options):
        test_obj = PageFactory.get_page_object("Zero",base_url=options.url)

        #Setup and register a driver
        test_obj.register_driver(options.remote_flag,options.os_name,options.os_version,options.browser,options.browser_version,options.remote_project_name,options.remote_build_name)

        #Setup TestRail reporting
        if options.testrail_flag.lower()=='y':
            if options.test_run_id is None:
                test_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest -X Y -R 100\n"+'\033[0m')
                options.testrail_flag = 'N'
            if options.test_run_id is not None:
                test_obj.register_testrail()
                test_obj.set_test_run_id(options.test_run_id)

        if options.tesults_flag.lower()=='y':
            test_obj.register_tesults()

        test_example_form(test_obj)

        #teardowm
        test_obj.wait(3)
        test_obj.teardown()
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(option_obj.print_usage())
