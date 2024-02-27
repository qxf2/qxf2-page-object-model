"""
Utility function which is used to summarize the Pytest results using Large Langauge Model, GPT-4.

Steps to Use:
Generate test log file by adding ">log/pytest_log_file.log" command at end of pytest command
Example: python -m pytest -k example_form --summary y --capture=tee-sys > log/pytest_log_file.log

Note: Your terminal must be pointed to root address (qxf2-page-object-model)
while generating test report file using above command
"""

import os, sys
import json
from openai import OpenAI, OpenAIError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf.gpt_summarization_prompt import summarization_prompt

API_KEY = os.getenv("API_KEY")
CLIENT = OpenAI(api_key=API_KEY)
MODEL = "gpt-4-1106-preview"


def get_gpt_response(results_log_file):
    """
    Generate GPT response for summary based on test results.

    Args:
    results_log_file (str): The file containing the test results.

    Returns:
    str: The GPT response based on the test results.
    """

    # Example to show how the summary results JSON format should be
    example_test_results = {
            "SummaryOfTestResults": {
                "PassedTests": ["test_name_1", "test_name_2"],
                "FailedTests": [
                    {
                        "test_name": "test_name_3",
                        "reasons_for_failure": [
                            "error message 1",
                            "error message 2"
                        ],
                        "recommendations": [
                            "suggestion 1",
                            "suggestion 2"
                        ]
                    },
                    {
                        "test_name": "test_name_4",
                        "reasons_for_failure": [
                            "error message 1",
                            "error message 2"
                        ],
                        "recommendations": [
                            "suggestion 1",
                            "suggestion 2"
                        ]
                    }
                    # ... Additional failed tests
                ]
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
        return

    # Send a request to the OpenAI API while providing the system prompt and the log file contents (as input message)
    try:
        response = CLIENT.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_message},
            ],
            max_tokens=None,
        )

        # Get the response content from the API
        response = response.choices[0].message.content
        response = json.dumps(response)
        return response
    except OpenAIError as api_error:
        print(f"OpenAI API Error: {api_error}")
        return

def generate_html_report(json_string):
    # Load the JSON data
    data = json.loads(json_string)

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
            .test-list li:before { content: "• "; }
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

    # Extract and format the summary of test results
    summary = data.get("SummaryOfTestResults", {})
    passed_tests = summary.get("PassedTests", [])
    failed_tests = summary.get("FailedTests", [])

    # Passed Tests Section
    if passed_tests:
        html_content += "<h2 class='heading'>Passed Tests</h2>"
        html_content += "<ul class='test-list'>"
        for i, test in enumerate(passed_tests, start=1):
            html_content += f"<li class='test-name'>{i}. {test}</li>"
        html_content += "</ul>"
    else:
        html_content += "<h2 class='heading'>Passed Tests</h2><p>None</p>"

    # Failed Tests Section
    if failed_tests:
        html_content += "<h2 class='heading'>Failed Tests</h2>"
        html_content += "<div class='failed-tests'>"
        html_content += "<table>"
        html_content += "<tr><th>Test Name</th><th>Reasons for Failure</th><th>Recommendations</th></tr>"
        for test in failed_tests:
            html_content += "<tr>"
            html_content += f"<td>{test['test_name']}</td>"
            reasons = '<br>'.join([f"<li>{reason}</li>" for reason in test.get("reasons_for_failure", [])])
            recommendations = '<br>'.join([f"<li>{recommendation}</li>" for recommendation in test.get("recommendations", [])])
            html_content += f"<td><ul class='reasons'>{reasons}</ul></td>"
            html_content += f"<td><ul class='recommendations'>{recommendations}</ul></td>"
            html_content += "</tr>"
        html_content += "</table>"
        html_content += "</div>"
    else:
        html_content += "<h2 class='heading'>Failed Tests</h2><p>None</p>"

    # Close the HTML content
    html_content += """
    </body>
    </html>
    """

    return html_content


#TODO: Implement try catch for this function
def generate_gpt_summary():
    # Get the directory of the current module and define paths for input log file and output summary file
    module_path = os.path.dirname(__file__)

    test_run_log_file = os.path.abspath(
        os.path.join(module_path, "..", "log", "multiple_tests_incorrect_url.txt")
    )

    gpt_summary_file = os.path.abspath(
        os.path.join(module_path, "..", "tests", "gpt_summary.html")
    )

    # Generate GPT response based on input log file
    gpt_response = get_gpt_response(test_run_log_file)
    print("GPT Response", gpt_response)

    # Generate HTML report for the GPT response
    html_report = generate_html_report(gpt_response)

    with open(gpt_summary_file, 'w') as file:
        file.write(html_report)
    
    print("Results summary generated in gpt_summary.html")

# ---USAGE EXAMPLES
if __name__ == "__main__":
    generate_gpt_summary()