"""
This test file runs accessibility checks on multiple pages of the Selenium tutorial pages using Axe.
It compares the Axe violation results to previously saved snapshots to identify new violations.
If new violations are found, they are logged in a violation record file.
Pages tested:
    1. Selenium tutorial main page
    2. Selenium tutorial redirect page
    3. Selenium tutorial contact page
"""
import os
import sys
import pytest
from utils.snapshot_util import Snapshotutil
from page_objects.PageFactory import PageFactory
import conf.snapshot_dir_conf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

@pytest.mark.ACCESSIBILITY
def test_accessibility(test_obj):
    "Test accessibility using Axe and compare snapshot results and save if new violations found"
    try:

        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #Create an instance of the Snapshotutil class
        snapshot_util = Snapshotutil()
        #Set up the violations log file
        violations_log_path = snapshot_util.initialize_violations_log()
        snapshot_dir = conf.snapshot_dir_conf.snapshot_dir

        #Get all pages
        page_names = conf.snapshot_dir_conf.page_names
        for page in page_names:
            test_obj = PageFactory.get_page_object(page,base_url=test_obj.base_url)
            #Inject Axe in every page
            test_obj.accessibility_inject_axe()
            #Check if Axe is run in every page
            axe_result = test_obj.accessibility_run_axe()
            #Extract the 'violations' section from the Axe result
            current_violations = axe_result.get('violations', [])
            #Load the existing snapshot for the current page (if available)
            existing_snapshot = snapshot_util.initialize_snapshot(snapshot_dir, page, current_violations=current_violations)

            #Compare the current violations with the existing snapshot to find any new violations
            snapshots_match, new_violation_details = snapshot_util.compare_and_log_violation(
                    current_violations, existing_snapshot, page, violations_log_path
                )
            #For each new violation, log few details to the output display
            if new_violation_details:
                snapshot_util.log_new_violations(new_violation_details)
            #Log the result of the comparison (pass or fail) for the current page
            test_obj.log_result(snapshots_match,
                                 positive=f'Accessibility checks for {page} passed',
                                 negative=f'Accessibility checks for {page} failed',
                                 level='debug')

        #Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        test_obj.log_result(
            False,
            positive="",
            negative=f"Exception when trying to run test: {__file__}\nPython says: {str(e)}",
            level='error'
        )

    assert expected_pass == actual_pass, f"Test failed: {__file__}"
