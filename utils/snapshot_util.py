"""
Snapshot Integration
* This is a class which extends the methods of Snapshot parent class
"""
import os
import json
from loguru import logger
from deepdiff import DeepDiff
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

    def log_violations_to_file(self, new_violation_details, violations_log_path):
        "Log violations in to a text file"
        try:
            with open(violations_log_path, 'a', encoding='utf-8') as log_file:
                for violation in new_violation_details:
                    violation_message = self.format_violation_message(violation)
                    # Write complete violation message to file
                    log_file.write(violation_message)
        except Exception as e:
            print(f"Error while logging violations: {e}")

    def format_violation_message(self, violation):
        "Format the violation message into a string."
        return (
            f"Violations on page: {violation['page']}\n"
            f"Description: {violation['description']}\n"
            f"Violation ID: {violation['id']}\n"
            f"Violation Root: {violation['key']}\n"
            f"Impact: {violation['impact']}\n"
            f"nodes: {violation['nodes']}\n\n"
        )

    def initialize_snapshot(self, snapshot_dir, page, current_violations=None):
        "Initialize the snapshot for a given page."
        snapshot_file_path = self.get_snapshot_path(snapshot_dir, page)
        if not os.path.exists(snapshot_dir):
            os.makedirs(snapshot_dir)
        existing_snapshot = self.load_snapshot(snapshot_file_path)
        # Save a new snapshot if none exists
        if existing_snapshot is None and current_violations is not None:
            self.save_snapshot(snapshot_file_path, current_violations)
            return None

        return existing_snapshot

    def compare_and_log_violation(self, current_violations, existing_snapshot, page, log_path):
        "Compare current violations against the existing snapshot."

        # Convert JSON strings to Python dictionaries
        current_violations_dict = {item['id']: item for item in current_violations}
        existing_snapshot_dict = {item['id']: item for item in existing_snapshot}

        # Use deepdiff to compare the snapshots
        violation_diff = DeepDiff(existing_snapshot_dict,
                                  current_violations_dict,
                                  ignore_order=True,
                                  verbose_level=2)

        # If there is any difference, it's a new violation
        if violation_diff:
            # Log the differences (you can modify this to be more specific or detailed)
            new_violation_details = self.extract_diff_details(violation_diff, page)
            self.log_violations_to_file(new_violation_details, log_path)
            return False, new_violation_details

        # If no difference is found
        return True, []

    def extract_diff_details(self, violation_diff, page):
        "Extract details from the violation diff."
        violation_details = []

        # Handle newly added violations (dictionary_item_added)
        for key, value in violation_diff.get('dictionary_item_added', {}).items():
            violation_details.append({
                "page": f"{page}- New violation added",
                "id": value['id'],
                "key": key,
                "impact": value.get('impact', 'Unknown'),
                "description": value.get('description', 'Unknown'),
                "nodes": value.get('nodes', 'Unknown')
            })

        # Handle removed violations (dictionary_item_removed)
        for key, value in violation_diff.get('dictionary_item_removed', {}).items():
            violation_details.append({
                "page": f"{page}- Violation resolved",
                "id": value['id'],
                "key": key,
                "impact": value.get('impact', 'Unknown'),
                "description": value.get('description', 'Unknown'),
                "nodes": value.get('nodes', 'Unknown')
            })

        # Handle changes to existing violations (values_changed)
        for key, value in violation_diff.get('values_changed', {}).items():
            path = key.split("']")[-2]
            old_value = value['old_value']
            new_value = value['new_value']
            violation_details.append({
                "page": f"{page}- Violation Node updated",
                "id": path,
                "key": key,
                "impact": value.get('new_value', 'Unknown'),
                "description": f"Changed from- {old_value} \n\t\t To- {new_value}",
                "nodes": key
            })

        # Handle added items in iterable (iterable_item_added)
        for key, value in violation_diff.get('iterable_item_added', {}).items():
            violation_details.append({
                "page": f"{page}- Violation Node added",
                "id": value.get('id', 'Unknown'),
                "key": key,
                "impact": value.get('impact', 'Unknown'),
                "description": f"New node item added: {key}",
                "nodes": str(value)
            })

        # Handle removed items in iterable (iterable_item_removed)
        for key, value in violation_diff.get('iterable_item_removed', {}).items():
            violation_details.append({
                "page": f"{page}- Violation Node resolved",
                "id": value.get('id', 'Unknown'),
                "key": key,
                "impact": value.get('impact', 'Unknown'),
                "description": f"Item node removed: {key}",
                "nodes": str(value)
            })

        return violation_details

    def log_new_violations(self, new_violation_details):
        "Log details of new violations to the console."
        for violation in new_violation_details:
            violation_message = self.format_violation_message(violation)
            # Print a truncated message to the console
            logger.info(f"{violation_message[:120]}..."
                        "Complete violation output is saved"
                        "in ../conf/new_violations_record.txt")
