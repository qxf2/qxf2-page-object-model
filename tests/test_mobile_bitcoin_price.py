"""
Automated test will do the following:
    # Open Bitcoin Info application in emulator.
    # Click on the bitcoin real time price page button.
    # Compare expected bitcoin real time price page heading with current page heading.
    # Verify that the bitcoin real time price is displayed on the page.
    # Display the results.
"""
import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects import PageFactory
import conf.mobile_bitcoin_conf as conf
import pytest

@pytest.mark.MOBILE
def test_mobile_bitcoin_price(test_mobile_obj):
    "Run the test."
    try:
        # Initalize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object.
        test_obj = PageFactory.get_page_object("bitcoin main page")

        #2. Setup and register a driver
        start_time = int(time.time())

        #3. Get expected bitcoin price page header name
        expected_bitcoin_price_page_heading = conf.expected_bitcoin_price_page_heading

        #4. Click on real time price page button and verify the price page header name.
        result_flag = test_obj.click_on_real_time_price_button(expected_bitcoin_price_page_heading)
        test_obj.log_result(result_flag,
                    positive="Successfully visited the bitcoin real time price page.",
                    negative="Failed to visit the bitcoin real time price page.")

        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))

        #5. Verify bitcoin real time price is displayed.
        if result_flag is True:
            result_flag = test_obj.get_bitcoin_real_time_price()
        test_obj.log_result(result_flag,
                            positive="Successfully got the bitcoin real time price in usd.",
                            negative="Failed to get the bitcoin real time price in usd.")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))

        #6. Print out the results.
        test_obj.write_test_summary()

        #7. Teardown and Assertion.
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print("Exception when trying to run test:%s" % __file__)
        print("Python says:%s" % str(e))

    assert expected_pass == actual_pass,"Test failed: %s"%__file__