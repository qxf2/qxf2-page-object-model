"""
This is an example automated test to help you learn Qxf2's framework
Our automated test will do the following:
    #Open Qxf2 selenium-tutorial-main page.
    #Fill the example form.
    #Click on Click me! button and check if its working fine.
"""
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects import PageFactory
import conf.example_form_conf as conf
import pytest


@pytest.mark.GUI
def test_example_form(test_obj):

    "Run the test"
    try:
        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object and fill the example form.
        test_obj = PageFactory.get_page_object("Main Page", base_url=test_obj.base_url)
        #Set start_time with current time
        start_time = int(time.time())

        #4. Get the test details from the conf file
        name = conf.name
        email = conf.email
        phone = conf.phone_no
        gender = conf.gender

        #5. Set name in form
        result_flag = test_obj.set_name(name)
        test_obj.log_result(result_flag,
                            positive="Name was successfully set to: %s\n"%name,
                            negative="Failed to set name: %s \nOn url: %s\n"%(name,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        test_obj.add_tesults_case("Set Name", "Sets the name in the form", "test_example_form", result_flag, "Failed to set name: %s \nOn url: %s\n"%(name,test_obj.get_current_url()), [test_obj.log_obj.log_file_dir + os.sep + test_obj.log_obj.log_file_name])
        #6. Set Email in form
        result_flag = test_obj.set_email(email)
        test_obj.log_result(result_flag,
                            positive="Email was successfully set to: %s\n"%email,
                            negative="Failed to set Email: %s \nOn url: %s\n"%(email,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        test_obj.add_tesults_case("Set Email", "Sets the email in the form", "test_example_form", result_flag, "Failed to set Email: %s \nOn url: %s\n"%(email,test_obj.get_current_url()), [], {'Email': email}, {'_Email': email})

        #7. Set Phone number in form
        result_flag = test_obj.set_phone(phone)
        test_obj.log_result(result_flag,
                            positive="Phone number was successfully set for phone: %s\n"%phone,
                            negative="Failed to set phone number: %s \nOn url: %s\n"%(phone,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        test_obj.add_tesults_case("Set Phone Number", "Sets the phone number in the form", "test_example_form", result_flag, "Failed to set phone number: %s \nOn url: %s\n"%(phone,test_obj.get_current_url()), [], {}, {'_Phone': phone, '_AnotherCustomField': 'Custom field value'})

        #8. Set Gender in form
        result_flag = test_obj.set_gender(gender)
        test_obj.log_result(result_flag,
                            positive= "Gender was successfully set to: %s\n"%gender,
                            negative="Failed to set gender: %s \nOn url: %s\n"%(gender,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        test_obj.add_tesults_case("Set Gender", "Sets the gender in the form", "test_example_form", result_flag, "Failed to set gender: %s \nOn url: %s\n"%(gender,test_obj.get_current_url()), [])

        #9. Check the copyright
        result_flag = test_obj.check_copyright()
        test_obj.log_result(result_flag,
                            positive="Copyright check was successful\n",
                            negative="Copyright looks wrong.\nObtained the copyright%s\n"%test_obj.get_copyright())
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        test_obj.add_tesults_case("Check copyright", "Checks the copyright", "test_example_form", result_flag, "Copyright looks wrong.\nObtained the copyright%s\n"%test_obj.get_copyright(), [])

        #10. Set and submit the form in one go
        result_flag = test_obj.submit_form(name,email,phone,gender)
        test_obj.log_result(result_flag,
                            positive="Successfully submitted the form\n",
                            negative="Failed to submit the form \nOn url: %s"%test_obj.get_current_url(),
                            level="critical")
        test_obj.add_tesults_case("Submit Form", "Submits the form", "test_example_form", result_flag,"Failed to submit the form \nOn url: %s"%test_obj.get_current_url(), [])

        #11. Check the heading on the redirect page
        #Notice you don't need to create a new page object!
        if result_flag is True:
            result_flag = test_obj.check_heading()
        test_obj.log_result(result_flag,
                            positive="Heading on the redirect page checks out!\n",
                            negative="Fail: Heading on the redirect page is incorrect!")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        test_obj.add_tesults_case("Check Heading", "Checks the heading on the redirect page", "test_example_form", result_flag,"Fail: Heading on the redirect page is incorrect!", [])

        #12. Visit the contact page and verify the link
        result_flag = test_obj.goto_footer_link('Contact > Get in touch!','contact')
        test_obj.log_result(result_flag,
                            positive="Successfully visited the Contact page\n",
                            negative="\nFailed to visit the Contact page\n")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        test_obj.add_tesults_case("Contact page", "Visits the contact page and verifies the link", "test_example_form", result_flag,"\nFailed to visit the Contact page\n")

        #13. Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

    assert expected_pass == actual_pass, "Test failed: %s"%__file__
