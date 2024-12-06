"""
This is a test file to run accessibility test on
    1. Selenium tutorial main page
    2. Selenium tutorial redirect page
    3. Selenium tutorial contact page
    #While running the test for first time, use --snapshot-update to create a snapshot folder
"""
import os
import sys
import json
import pytest
from utils.snapshot_util import Snapshotutil
from page_objects.PageFactory import PageFactory
import conf.snapshot_dir_conf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

@pytest.mark.ACCESSIBILITY
def test_accessibility(test_obj):
    "Inject Axe and create snapshot for every page"
    try:

        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #Create an instance of the Snapshotutil class
        snapshot_util = Snapshotutil()
        # Set up the violations log file
        violations_log_path = snapshot_util.initialize_violations_log()
        snapshot_dir = conf.snapshot_dir_conf.snapshot_dir

        #Get all pages
        page_names = PageFactory.get_all_page_names()
        for page in page_names:
            test_obj = PageFactory.get_page_object(page,base_url=test_obj.base_url)
            #Inject Axe in every page
            test_obj.accessibility_inject_axe()
            #Check if Axe is run in every page
            axe_result = test_obj.accessibility_run_axe()
            #Extract only the violations section
            current_violations = axe_result.get('violations', [])
            #Snapshot file path to load
            existing_snapshot, snapshot_file_path = snapshot_util.initialize_snapshot(snapshot_dir,
                                                                                      page)

            #If snapshot does not exist, create a new one
            if existing_snapshot is None:
                snapshot_util.save_snapshot(snapshot_file_path, current_violations)
                # Re-load the snapshot after saving it so the comparison can happen
                test_obj.log_result(
                    True,  # Treat as passed since this is expected behavior
                    positive=(
                        f"No existing snapshot was found for {page}."
                        "A new snapshot has been created in ../conf/snapshot dir"
                        "Please review the snapshot for violations before running the test again."
                    ),
                    negative="",
                    level='info'
                )
                continue

            snapshots_match, new_violation_details = snapshot_util.compare_violation(
                    current_violations, existing_snapshot, page, violations_log_path
                )

            for violation in new_violation_details:
                violation_message = (
                    f"New violations found on: {violation['page']}\n"
                    f"Violation ID: {violation['id']}\n"
                    f"Impact: {violation['impact']}\n"
                    f"Description: {violation['description']}\n"
                    f"HTML Snippet: {violation['html']}\n\n"
                )
                test_obj.log_result(
                    False,
                    positive="",
                    negative=(
                        f"{violation_message[:80]}..."
                        "Complete violation output is saved in"
                        "../conf/new_violations_record.txt"
                    ),
                    level='debug'
                )

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
