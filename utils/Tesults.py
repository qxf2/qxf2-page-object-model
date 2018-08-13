import tesults
import conf.tesults_conf as conf_file

cases = []

def add_test_case(data):
    cases.append(data)

def post_results_to_tesults ():
    token = conf_file.target_token_default # uses default token unless otherwise specified
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