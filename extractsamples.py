from googleapiclient.discovery import build
import httplib2
import re, sys
import isb_auth
import pdb;pdb.set_trace()

def get_unauthorized_service():
        api = 'isb_cgc_api'
        version = 'v2'
        site = 'https://api-dot-isb-cgc.appspot.com'
        discovery_url = '%s/_ah/api/discovery/v1/apis/%s/%s/rest'\
                         % (site, api, version)
        return build(api, version, \
                discoveryServiceUrl=discovery_url, \
                http=httplib2.Http())


def fetch_cohort_data(p_bcodes):

    """
    Take a set of list of patient barcodes and fetch any possible
    data associated with them. Returns a list of dictionaries,
    each dictionary corresponds 
    """


    all_data= list()
    service = get_unauthorized_service()

    for bcode in p_bcodes:
        data = service.samples().get(sample_barcode=bcode).execute()
        all_data.append(data)
    return all_data

# all_data in this case is a list of dictionaries
# Each dictionary corresponds to one barcode
# For most dicts, these are the keys (a couple are missing a field):
# [u'kind', u'patient', u'data_details', u'data_details_count', u'etag', u'aliquots', u'biospecimen_data'] 

# all_data[1]['data_details'][2]['cloud_storage_path']  < give a path to a file

# The number '2' designates a file. 


def get_dtypes(num):
    """
    Gets the available data types for each patient barcode, 
    by it's num in the array, each Datatype has a access level and
    cloud_storage_path. 
    """
    # Can get len also from all_data[num]['data_details_count']
    # for i in range(len(all_data[num]['data_details'])): 
        # print all_data[num]['data_details'][i]['Datatype']

    for i in range(all_data[num]['data_details_count']): 
        print all_data[num]['data_details'][i]['SecurityProtocol'] \
                +'\t\t'\
                + all_data[num]['data_details'][i]['Datatype']


__if__=='__main__':

    inp = open(sys.argv[1])

    inpt= inp.read()

    buf = inpt.split("samples")[1]
    buf = buf.split("]")[0]
    res = re.findall('TCGA.*"', buf)
    res = [x.replace('"','') for x in res]

    p_mdata = fetch_cohort_data(res)




