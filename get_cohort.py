# Python:

import isb_auth
import isb_curl
import sys
import requests

url = 'https://isb-cgc.appspot.com/_ah/api/cohort_api/v1/cohorts_list'
token = isb_curl.get_access_token()
head = {'Authorization': 'Bearer ' + token}

# for GET requests
# resp = requests.get(url, headers=head)
# querystring parameters can be added to either the url itself...
# url += '?cohort_id=1'

# resp = requests.get(url, headers=head)
# ... or passed in with the params kwarg
# url = 'https://isb-cgc.appspot.com/_ah/api/cohort_api/v1/cohorts_list'
params = {'cohort_id': 1}
url = "https://api-dot-isb-cgc.appspot.com/_ah/api/isb_cgc_api/v2/cohorts/932"
# resp = requests.get(url, headers=head, params=params)
resp = requests.get(url, headers=head)
con = resp.content

if len(sys.argv) != 2:
    print 'usage: get_cohorts.py [outfile]'
    sys.exit(1)

fp = open(sys.argv[1], 'w')
fp.write(con)

# import pdb; pdb.set_trace()
# if the endpoint takes a resource in the request body, such as the save_cohort endpoint...
# url = 'https://isb-cgc.appspot.com/_ah/api/cohort_api/v1/save_cohort?name=my-new-cohort'
# head.update({'Content-Type': 'application/json'})
# payload = {"SampleBarcode": "TCGA-02-0001-01C,TCGA-02-0001-10A,TCGA-01-0642-11A"}
# resp = requests.post(url, headers=head, json=payload)
# 
# # if requests version < 2.4.2
# import json
# resp = requests.post(url, headers=head, data=json.dumps(payload))
# 
# 
# 
