import os
import tesults

cases = []

def add_test_case(data):
    cases.append(data)

def post_results_to_tesults ():
    " This method is to post the results into the tesults"
    # uses default token unless otherwise specified
    token = os.getenv('tesults_target_token_default')
    if token is None:
        solution =("It looks like you are trying to use tesults to run your test."
                   "Please make sure you have updated .env with the right credentials .")
        print(f"\033[92m\nSOLUTION: {solution}\n\033[0m")
    else:
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
        