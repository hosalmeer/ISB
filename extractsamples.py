from googleapiclient.discovery import build
import httplib2
import re, sys

inp = open(sys.argv[1])

inpt= inp.read()

buf = inpt.split("samples")[1]
buf = buf.split("]")[0]
res = re.findall('TCGA.*"', buf)
res = [x.replace('"','') for x in res]

def get_unauthorized_service():
        api = 'isb_cgc_api'
        version = 'v2'
        site = 'https://api-dot-isb-cgc.appspot.com'
        discovery_url = '%s/_ah/api/discovery/v1/apis/%s/%s/rest' % (site, api, version)
        return build(api, version, discoveryServiceUrl=discovery_url, http=httplib2.Http())

service = get_unauthorized_service()
all_data= list()

for bcode in res:
    data = service.samples().get(sample_barcode=bcode).execute()
    print data
    all_data.append(data)




