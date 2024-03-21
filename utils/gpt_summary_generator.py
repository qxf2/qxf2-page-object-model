"""
Utility function which is used to summarize the Pytest results using LLM (GPT-4).
And provide recommendations for any failures encountered.
The input for the script is a log file containing the detailed Pytest results.
It then uses the OpenAI API to generate a summary based on the test results.
The summary is written to a html file.

Usage:
    python gpt_summary_generator.py

Note:
OPENAI_API_KEY must be provided.
At the time of writing, the model used is "gpt-4-1106-preview".
The prompt used to generate the summary is in conf/gpt_summarization_prompt.py file.
The max_tokens is set to None.
"""

import os
import sys
import json
from openai import OpenAI, OpenAIError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf.gpt_summarization_prompt import summarization_prompt


def get_gpt_response(client, model, results_log_file):
    """
    Generate GPT response for summary based on test results.
    Args:
    - client (OpenAI): The OpenAI client.
    - model (str): The GPT model to use.
    - results_log_file (str): The file containing the test results.
    Returns:
    - gpt_response (str): The response generated by the GPT model.
    """

    # Example to show how the summary results JSON format should be
    example_test_results = {
        "SummaryOfTestResults": {
            "PassedTests": {
                "test_name_1": "{{number_of_checks_passed}}",
                "test_name_2": "{{number_of_checks_passed}}"
            },
            "FailedTests": [
                {
                    "test_name": "test_name_3",
                    "reasons_for_failure": ["error message 1", "error message 2"],
                    "recommendations": ["suggestion 1", "suggestion 2"],
                },
                {
                    "test_name": "test_name_4",
                    "reasons_for_failure": ["error message 1", "error message 2"],
                    "recommendations": ["suggestion 1", "suggestion 2"],
                }
                # ... Additional failed tests
            ],
        }
    }

    example_test_results_json = json.dumps(example_test_results)

    # Create the system prompt
    system_prompt = summarization_prompt + example_test_results_json

    # Open the results log file and read its contents
    try:
        with open(results_log_file, "r") as file:
            input_message = file.read()
    except FileNotFoundError as file_error:
        print(f"Error: Test report file not found - {file_error}")
        return None

    # Send a request to OpenAI API
    try:
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_message},
            ],
            max_tokens=None,
        )
        response = response.choices[0].message.content
        return response
    except OpenAIError as api_error:
        print(f"OpenAI API Error: {api_error}")
        return None


def generate_html_report(json_string):
    """
    Generate an HTML report from a JSON string representing test results.
    Args:
    - json_string (str): A JSON string representing test results.
    Returns:
    - html_content (str): An HTML report with the summary of passed and failed tests.
    """
    # Load the JSON data
    try:
        data = json.loads(json_string)
    except TypeError as type_error:
        print(f"Error loading JSON data: {type_error}")
        return None

    # Initialize the HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Results Report</title>
        <style>
            body { font-family: Arial, sans-serif; }
            h2 { color: #333; }
            .passed-tests, .failed-tests { margin-bottom:   20px; }
            .test-list { list-style-type: none; padding:   0; }
            .test-list li { padding:   5px   0; }
            .test-list li:before { content: "* "; }
            .test-list li.test-name { font-weight: bold; }
            .failed-tests table { border-collapse: collapse; width:   100%; }
            .failed-tests th, .failed-tests td { border:   1px solid #ddd; padding:   8px; }
            .failed-tests th { background-color: #f2f2f2; }
            .failed-tests .reasons, .failed-tests .recommendations { list-style-type: disc; margin-left:  20px; }
            .heading { color: #000080; }
        </style>
    </head>
    <body>
    """

    try:
        # Extract and format the summary of test results
        summary = data.get("SummaryOfTestResults", {})
        passed_tests = summary.get("PassedTests", {})
        failed_tests = summary.get("FailedTests", [])

        # Passed Tests Section
        html_content += "<h2 class='heading'>Passed Tests</h2>"
        if passed_tests:
            html_content += "<ul class='test-list'>"
            for test_name, num_checks_passed in passed_tests.items():
                html_content += f"<li class='test-name'>{test_name} ({num_checks_passed} checks)</li>"
            html_content += "</ul>"
        else:
            html_content += "<p>None</p>"

        # Failed Tests Section
        if failed_tests:
            html_content += "<h2 class='heading'>Failed Tests</h2>"
            html_content += "<div class='failed-tests'>"
            html_content += "<table>"
            html_content += "<tr><th>Test Name</th><th>Reasons for Failure</th><th>Recommendations</th></tr>"
            for test in failed_tests:
                html_content += "<tr>"
                html_content += f"<td>{test['test_name']}</td>"
                reasons = "<br>".join(
                    [
                        f"<li>{reason}</li>"
                        for reason in test.get("reasons_for_failure", [])
                    ]
                )
                recommendations = "<br>".join(
                    [
                        f"<li>{recommendation}</li>"
                        for recommendation in test.get("recommendations", [])
                    ]
                )
                html_content += f"<td><ul class='reasons'>{reasons}</ul></td>"
                html_content += (
                    f"<td><ul class='recommendations'>{recommendations}</ul></td>"
                )
                html_content += "</tr>"
            html_content += "</table>"
            html_content += "</div>"
        else:
            html_content += "<h2 class='heading'>Failed Tests</h2><p>None</p>"

    except KeyError as key_error:
        print(f"Key error encountered: {key_error}")
        return None

    # Close the HTML content
    html_content += """
    </body>
    </html>
    """

    return html_content


def generate_gpt_summary():
    """
    Generate GPT response based on input log file and create a summary HTML report.
    """
    # Get the paths of the files
    module_path = os.path.dirname(__file__)

    test_run_log_file = os.path.abspath(
        os.path.join(module_path, "..", "log", "consolidated_log.txt")
    )

    gpt_summary_file = os.path.abspath(
        os.path.join(module_path, "..", "log", "gpt_summary.html")
    )

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    model = "gpt-4-1106-preview"

    # Generate GPT response based on input log file
    gpt_response = get_gpt_response(client, model, test_run_log_file)

    # Generate HTML report for the GPT response
    if gpt_response:
        html_report = generate_html_report(gpt_response)

        with open(gpt_summary_file, "w") as file:
            file.write(html_report)
        print(
            "\n Results summary generated in gpt_summary.html present under log directory \n"
        )
    else:
        print("Error: No GPT response generated")

# ---USAGE---
if __name__ == "__main__":
    generate_gpt_summary()
