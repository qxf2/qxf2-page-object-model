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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.mark.ACCESSIBILITY
def test_accessibility(test_obj):
    "Inject Axe and create snapshot for every page"
    try:

        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #Create an instance of the Snapshotutil class
        snapshot_util = Snapshotutil()
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
            snapshot_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..',
                'utils',
                'snapshot'
            )
            snapshot_file_path = os.path.join(
                snapshot_dir,
                f'snapshot_output_{page}.json'
            )

            if not os.path.exists(snapshot_dir):
                os.makedirs(snapshot_dir)

            existing_snapshot = snapshot_util.load_snapshot(snapshot_file_path)

            #If snapshot does not exist, create a new one
            if existing_snapshot is None:
                snapshot_util.save_snapshot(snapshot_file_path, current_violations)
                # Re-load the snapshot after saving it so the comparison can happen
                existing_snapshot = snapshot_util.load_snapshot(snapshot_file_path)

            #Formating the violation result and saved snapshot to json
            current_violations_json = json.dumps(current_violations, ensure_ascii=False, separators=(',', ':'))
            existing_snapshot_json = json.dumps(existing_snapshot, ensure_ascii=False, separators=(',', ':'))

            #Check if there are new violations
            new_violation = snapshot_util.find_new_violations(current_violations, existing_snapshot)
            if new_violation:
                new_violation_detail = snapshot_util.get_new_violations(current_violations_json, existing_snapshot_json, page)
                for violation in new_violation_detail:
                    test_obj.log_result(
                        False,
                        positive="",
                        negative=(
                            f"New violation found on {violation['page']} - "
                            f"ID: {violation['id']}, "
                            f"Impact: {violation['impact']}, "
                            f"Description: {violation['description']},"
                            f"HTML: {violation['html']}"
                        ),
                        level='error'
                    )

            #Comparison snapshot
            if current_violations_json != existing_snapshot_json:
                snapshots_match = False
            else:
                snapshots_match = True

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
