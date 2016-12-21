
import isb_auth
import isb_curl
import sys
import requests

def main():

    token = isb_curl.get_access_token()
    head = {'Authorization': 'Bearer ' + token}
    if len(sys.argv) != 3:
        print 'usage: get_cohorts.py [#cohort] [outfile]'
        sys.exit(1)

    params = {'cohort_id': 1}
    url = "https://api-dot-isb-cgc.appspot.com/_ah/api/isb_cgc_api/v2/cohorts/" + sys.argv[1]
    # resp = requests.get(url, headers=head, params=params)
    resp = requests.get(url, headers=head)
    con = resp.content
    
    return con

if __name__=="__main__":
    
    con = main()
    fp = open(sys.argv[2], 'w')
    fp.write(con)

