import requests
import boto3
import time
import os
import threading

expireBuffer = int(30) # 30 seconds

filesUploaded = 0
bytesUploaded = 0
uploading = []

def create_s3_client(credentials):
    s3Client = boto3.client(
        's3',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken'],
        region_name = 'us-east-1'
    )
    return s3Client


def refresh_credentials(target, key):
    data = {
        'target': target,
        'key': key
    }

    response = response = requests.post('https://www.tesults.com/permitupload', json=data)
    jsonResponse = response.json()
    
    if response.status_code != 200:
        failData = jsonResponse.get('error')
        message = failData.get('message')
        return {'success': False, 'message': message, 'upload': None}
    else:
        successData = jsonResponse.get('data')
        message = successData.get('message')
        upload = successData.get('upload')
        return {'success': True, 'message': message, 'upload': upload}
    

def files_upload(files, keyPrefix, auth, target):
    global filesUploaded
    global bytesUploaded
    global uploading

    class ProgressPercentage(object):
        def __init__(self, filename):
            self._filename = filename
            self._size = float(os.path.getsize(filename))
            self._seen_so_far = 0
            self._lock = threading.Lock()
        def __call__(self, bytes_amount):
            with self._lock:
                self._seen_so_far += bytes_amount
                if self._seen_so_far == self._size:
                    global filesUploaded
                    global bytesUploaded
                    global uploading
                    filesUploaded += 1
                    bytesUploaded += self._size
                    uploading.remove(self._filename)

    expirationString = auth.get('Expiration')
    expiration = int(expirationString)
    uploading = []
    warnings = []
    maxActiveUploads = 10 # Upload at most 10 files simultaneously to avoid hogging the client machine.
    s3 = create_s3_client(auth)

    while len(files) != 0 or len(uploading) != 0:
        try:
            if len(uploading) < maxActiveUploads and len(files) != 0:
                # check if new credentials required
                now = int(time.time())
                if now + expireBuffer > expiration: # check within 30 seconds of expiry
                    #refresh credentials here
                    if len(uploading) == 0:
                        # wait for all current transfers to complete so we can set a new transfer manager
                        response = refresh_credentials(target, keyPrefix)
                        
                        if response.get('success') != True:
                            # Must stop upload due to failure to get new credentails.
                            warnings.append(response['message'])
                            break
                        else:
                            upload = response.get('upload')
                            key = upload['key']
                            uploadMessage = upload['message']
                            permit = upload['permit']
                            auth = upload['auth']
                            if permit != True:
                                # Must stop upload due to failure to be permitted for new credentails.
                                warnings.append(uploadMessage)
                                break
                            else:
                                # Upload permitted
                                expirationString = auth.get('Expiration')
                                expiration = int(expirationString)
                                s3 = create_s3_client(auth)

                if now + expireBuffer < expiration:
                    # load new file for upload
                    file = files.pop(0)
                    if os.path.isfile(file['file']):
                        key = keyPrefix + "/" + str(file['num']) + "/" + os.path.basename(file['file'])
                        uploading.append(file['file'])
                        s3.upload_file(file['file'], "tesults-results", key, Callback=ProgressPercentage(file['file']))
                    else:
                        warnings.append('File not found: ' + file['file'])

            # check if existing uploads complete
            # handled in ProgressPercent callback
        except Exception as e:
            #warnings.append('Failed to upload file.')
            warnings.append(e)
    
    return {'message': 'Success. ' + str(filesUploaded) + ' files uploaded. ' + str(bytesUploaded) + ' bytes uploaded.', 'warnings': warnings}

def files_in_test_cases(data):
    results = data['results']
    cases = results['cases']
    files = []
    num = 0
    for c in cases:
        if 'files' in c:
            cfiles = c['files']
            for cfile in cfiles:
                retfile = {'num': num, 'file': cfile}
                files.append(retfile)
        num += 1
    return files

def results(data):
    global filesUploaded
    global bytesUploaded
    global uploading
    filesUploaded = 0
    bytesUploaded = 0
    uploading = []

    if type(data) != dict:
        message = "Results data must be a dictionary."
        return {'success': False, 'message': message, 'warnings': [], 'errors': [message]}
    
    response = requests.post('https://www.tesults.com/results', json=data)
    jsonResponse = None
    try:
        jsonResponse = response.json()
    except JSONDecodeError as e:
        errorMessage = 'Error saving test cases (Error: PY01), please contact support.'
        errors = []
        errors.append(errorMessage)
        return {'success': False, 'message': errorMessage, 'warnings': [], 'errors': errors}

    if response.status_code != 200:
        failData = jsonResponse.get('error')
        message = failData.get('message')
        return {'success': False, 'message': message, 'warnings': [], 'errors': [message]}
    else:
        successData = jsonResponse.get('data')
        messageResponse = successData.get('message')
        upload = successData.get('upload')
    
        if upload == None:
            # No files to upload, complete.
            return {'success': True, 'message': messageResponse, 'warnings': [], 'errors': []}
        else:
            # Upload files.
            target = data["target"]
            files = files_in_test_cases(data)

            key = upload.get('key')
            uploadMessage = upload.get('message')
            permit = upload.get('permit')
            auth = upload.get('auth')

            if permit != True:
                warnings = []
                warnings.append(uploadMessage)
                return {'success': True, 'message': messageResponse, 'warnings': warnings, 'errors': []}

            # upload required and permitted
            try:
                fileUploadReturn = files_upload(files, key, auth, target) # This can take a while
            except ValueError as e:
                warnings = []
                warnings.append(str(e))
                return {'success': True, 'message': e, 'warnings': warnings, 'errors':[]} 

            return {'success': True, 'message': fileUploadReturn['message'], 'warnings': fileUploadReturn['warnings'], 'errors':[]}