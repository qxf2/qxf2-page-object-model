"""
Snapshot Integration
* This is a class which extends the methods of Snapshot parent class
"""
import os
import json
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
        super().__init__(snapshot_update, allow_snapshot_deletion, snapshot_dir)

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
        new_violation_details = []

        for new_item in new_violations:
            for new_node in new_item['nodes']:
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
        return new_violation_details

    def initialize_violations_log(self, log_dir,
                                  log_filename: str = "new_violations_record.txt") -> str:
        "Initialize and clear the violations log file."
        log_path = os.path.join(log_dir, log_filename)
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("Accessibility Violations Log\n")
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
