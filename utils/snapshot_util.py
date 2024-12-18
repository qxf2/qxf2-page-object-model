"""
Snapshot Integration
* This is a class which extends the methods of Snapshot parent class
"""
import os
import json
import jsondiff
from datetime import datetime
from pytest_snapshot.plugin import Snapshot
import conf.snapshot_dir_conf

class Snapshotutil(Snapshot):
    "Snapshot object to use snapshot for comparisions"
    def __init__(self, snapshot_update=False,
                 allow_snapshot_deletion=False,
                 snapshot_dir=None):
        if snapshot_dir is None:
            snapshot_dir = conf.snapshot_dir_conf.snapshot_dir
        super().__init__(snapshot_update, allow_snapshot_deletion, snapshot_dir)
        self.snapshot_update = snapshot_update


    def load_snapshot(self, snapshot_file_path):
        "Load the saved snapshot from a JSON file."
        if os.path.exists(snapshot_file_path):
            with open(snapshot_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None

    def save_snapshot(self, snapshot_file_path, current_violations):
        "Save the given data as a snapshot in a JSON file."
        os.makedirs(os.path.dirname(snapshot_file_path), exist_ok=True)
        with open(snapshot_file_path, 'w', encoding='utf-8') as file:
            json.dump(current_violations, file, ensure_ascii=False, indent=4)

    def find_new_violations(self, current_violations, existing_snapshot):
        "Return a list of new violations that are not in the saved snapshot."
        new_violations = []
        for violation in current_violations:
            if violation not in existing_snapshot:
                new_violations.append(violation)
        return new_violations

    def sanitize_html(self, html):
        "Replace charmap characters so read html."
        return ''.join(c if ord(c) < 128 else '?' for c in html)

    def get_new_violations(self, current_violations_json, existing_snapshot_json, page):
        "Compares the snapshots and prints the new violations"
        # Load the results from JSON strings
        new_violations = json.loads(current_violations_json)
        saved_snapshot = json.loads(existing_snapshot_json)

        # Extract existing HTML elements from the saved snapshot
        existing_html_elements = self.extract_existing_html_elements(saved_snapshot)

        # Compare new violations and return details of new violations
        return self.compare_violations(new_violations, existing_html_elements, page)

    def extract_existing_html_elements(self, saved_snapshot):
        "Extracts existing HTML elements from the saved snapshot"
        existing_html_elements = set()
        for saved_item in saved_snapshot:
            for saved_node in saved_item['nodes']:
                if saved_node['any']:
                    for violation in saved_node['any']:
                        for related in violation['relatedNodes']:
                            existing_html_elements.add(related['html'])
        return existing_html_elements

    def compare_violations(self, new_violations, existing_html_elements, page):
        "Compares new violations with the existing HTML elements"
        # Set to track printed elements
        new_violation_details = []

        # Compare new violations and add new violation HTML elements not in the snapshot
        for new_item in new_violations:
            for new_node in new_item['nodes']:
                # Check violations in 'any' or if there are no related nodes
                if new_node['any'] or not new_node.get('relatedNodes'):
                    # Handle case where there are no related nodes but still need to log violation
                    if new_node['any']:
                        for violation in new_node['any']:
                            for related in violation['relatedNodes']:
                                # Add only if the HTML is not in the existing snapshot
                                if related['html'] not in existing_html_elements:
                                    sanitized_html = self.sanitize_html(related['html'])
                                    new_violation_details.append({
                                        "page": page,
                                        "id": new_item.get('id', 'unknown'),
                                        "impact": new_item.get('impact', 'unknown'),
                                        "description": new_item.get('description', 'unknown'),
                                        "html": sanitized_html
                                    })
                    else:
                        # If no related nodes, log the violation with no specific HTML element
                        new_violation_details.append({
                            "page": page,
                            "id": new_item.get('id', 'unknown'),
                            "impact": new_item.get('impact', 'unknown'),
                            "description": new_item.get('description', 'unknown'),
                            "html": new_node.get('html', 'No HTML available')
                        })
        return new_violation_details

    def initialize_violations_log(self,
                                  log_filename: str = "new_violations_record.txt") -> str:
        "Initialize and clear the violations log file."
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'conf')
        log_path = os.path.join(log_dir, log_filename)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"Accessibility Violations Log: {timestamp} \n")
            f.write("====================================\n")
        return log_path

    def get_snapshot_path(self, snapshot_dir: str, page_name: str) -> str:
        "Get the full path to the snapshot file for a given page."
        if not os.path.exists(snapshot_dir):
            os.makedirs(snapshot_dir)
        return os.path.join(snapshot_dir, f"snapshot_output_{page_name}.json")

    def log_violations_to_file(self, new_violation_detail, violations_log_path):
        "Log violations in to a text file"
        try:
            with open(violations_log_path, 'a', encoding='utf-8') as log_file:
                for violation in new_violation_detail:
                    violation_message = (
                        f"New violations found on: {violation['page']}\n"
                        f"Violation ID: {violation['id']}\n"
                        f"Impact: {violation['impact']}\n"
                        f"Description: {violation['description']}\n"
                        f"HTML Snippet: {violation['html']}\n\n"
                    )
                    # Write complete violation message to file
                    log_file.write(violation_message)
        except Exception as e:
            print(f"Error while logging violations: {e}")

    def initialize_snapshot(self, snapshot_dir, page):
        "Initialize the snapshot for a given page."
        snapshot_file_path = self.get_snapshot_path(snapshot_dir, page)
        if not os.path.exists(snapshot_dir):
            os.makedirs(snapshot_dir)
        existing_snapshot = self.load_snapshot(snapshot_file_path)

        return existing_snapshot

    def compare_and_log_violation(self, current_violations, existing_snapshot, page, log_path):
        "Compare current violations against the existing snapshot."
        current_violations_json = json.dumps(current_violations,
                                             ensure_ascii=False,
                                             separators=(',', ':'))
        existing_snapshot_json = json.dumps(existing_snapshot,
                                            ensure_ascii=False,
                                            separators=(',', ':'))

        # Find new violations
        # Convert JSON strings to Python dictionaries
        current_violations_dict = json.loads(current_violations_json)
        existing_snapshot_dict = json.loads(existing_snapshot_json)

        # Use jsondiff to compare the two dictionaries
        diff = jsondiff.diff(existing_snapshot_dict, current_violations_dict)

        # Ensure the diff is serializable by calling serialize_diff
        diff = self.serialize_diff(diff)

        # If there is any difference, it's a new violation
        if diff:
            # Log the differences (you can modify this to be more specific or detailed)
            new_violation_details = self.extract_diff_details(diff, page)
            self.log_violations_to_file(new_violation_details, log_path)
            return False, new_violation_details

        # If no difference is found
        return True, []

    def extract_diff_details(self, diff, page):
        "Extract details from the JSON diff."
        violation_details = []

        for key, value in diff.items():
            if isinstance(value, dict):  # Nested differences
                # Check for newly added violations or modifications
                if 'any' in value:
                    for violation in value['any']:
                        violation_details.append({
                            "page": page,
                            "id": violation.get('id', 'unknown'),
                            "impact": violation.get('impact', 'unknown'),
                            "description": violation.get('description', 'unknown'),
                            "html": violation['relatedNodes'][0]['html'] if violation.get('relatedNodes') else 'No HTML available'
                        })
                else:
                    # Log modified or new elements without HTML
                    violation_details.append({
                        "page": page,
                        "id": key,
                        "impact": "Unknown",
                        "description": f"New or modified element: {key}",
                        "html": str(value)
                    })
            else:  # Simple differences
                violation_details.append({
                    "page": page,
                    "id": key,
                    "impact": "Unknown",
                    "description": f"New or modified element: {key}",
                    "html": str(value)
                })
        
        return violation_details

    def serialize_diff(self, diff):
        "Ensure diff is serializable by converting non-serializable objects."
        if isinstance(diff, dict):
            for key, value in diff.items():
                diff[key] = self.serialize_diff(value)
        elif isinstance(diff, list):
            return [self.serialize_diff(item) for item in diff]
        elif isinstance(diff, jsondiff.Symbol):
            return str(diff)  # Convert Symbol to string for serialization
        return diff

    def log_new_violations(self, new_violation_details, test_obj):
        "Log details of new violations to the console."
        for violation in new_violation_details:
            violation_message = (
                f"New violations found on: {violation['page']}\n"
                f"Description: {violation['description']}\n"
                f"HTML Snippet: {violation['html']}\n\n"
            )
            test_obj.write(f"{violation_message[:80]}..."
                        "Complete violation output is saved in"
                        "../conf/new_violations_record.txt"
                )
