import os
from dotenv import load_dotenv
import tesults


load_dotenv()

cases = []

def add_test_case(data):
    cases.append(data)

def post_results_to_tesults ():
    " This method is to post the results into the tesults"
    # uses default token unless otherwise specified
    token = os.getenv('tesults_target_token_default')
    data = {
        'target': token,
        'results': { 'cases': cases }
    }
    print ('-----Tesults output-----')
    if len(data['results']['cases']) > 0:
        print (data)
        print('Uploading results to Tesults...')
        ret = tesults.results(data)
        print ('success: ' + str(ret['success']))
        print ('message: ' + str(ret['message']))
        print ('warnings: ' + str(ret['warnings']))
        print ('errors: ' + str(ret['errors']))
    else:
        print ('No test results.')
        