'''
A Simple API util which used to post test reports on Slack Channel.

Steps to Use:
1. Generate Slack incoming webhook url by reffering our blog: https://qxf2.com/blog/post-pytest-test-results-on-slack/ & add url in our code
2. Generate test report log file by adding ">log/pytest_report.log" command at end of py.test command for e.g. py.test -k example_form -I Y -r F -v > log/pytest_report.log
Note: Your terminal must be pointed to root address of our POM while generating test report file using above command
3. Check you are calling correct report log file or not
'''
import json,os,requests 

def post_reports_to_slack():
        #To generate incoming webhook url ref: https://qxf2.com/blog/post-pytest-test-results-on-slack/
        url= "incoming webhook url"  #Add your Slack incoming webhook url here
    
        #To generate pytest_report.log file add ">pytest_report.log" at end of py.test command for e.g. py.test -k example_form -I Y -r F -v > log/pytest_report.log
        test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','log','pytest_report.log'))#Change report file name & address here

        with open(test_report_file, "r") as in_file:
                testdata = ""
                for line in in_file:
                        testdata = testdata + '\n' + line
                
        # Set Slack Pass Fail bar indicator color according to test results   
        if 'FAILED' in testdata:
            bar_color = "#ff0000"
        else:
            bar_color = "#36a64f"

        data = {"attachments":[
                            {"color": bar_color,
                            "title": "Test Report",
                            "text": testdata}
                            ]}
        json_params_encoded = json.dumps(data)
        slack_response = requests.post(url=url,data=json_params_encoded,headers={"Content-type":"application/json"})
        if slack_response.text == 'ok':
                print('\n Successfully posted pytest report on Slack channel')
        else:
                print('\n Something went wrong. Unable to post pytest report on Slack channel. Slack Response:', slack_response) 

        
#---USAGE EXAMPLES
if __name__=='__main__':
        post_reports_to_slack()
    
