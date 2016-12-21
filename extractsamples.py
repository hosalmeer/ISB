from googleapiclient.discovery import build
import httplib2
import re, sys
import isb_auth


def get_unauthorized_service():
    """
    Copy-paste from the isb-cgc examples
    """
    api = 'isb_cgc_api'
    version = 'v2'
    site = 'https://api-dot-isb-cgc.appspot.com'
    discovery_url = '%s/_ah/api/discovery/v1/apis/%s/%s/rest'\
        % (site, api, version)
    return build(api, version, \
        discoveryServiceUrl=discovery_url, \
        http=httplib2.Http())


def fetch_patients(p_bcodes):

    """
    Take a set of list of patient barcodes and fetch any possible
    data associated with them. Returns a list of dictionaries,
    each dictionary corresponds 
    """

    print "\nPATIENT\n"

    all_data= list()
    service = get_unauthorized_service()

    for bcode in p_bcodes:
        data = service.patients().get(patient_barcode=bcode).execute()
        all_data.append(data)

    return all_data

def fetch_csamples(bcodes):

    """
    Take a set of list of sample barcodes and fetch any possible
    data associated with them. Returns a list of dictionaries,
    each dictionary corresponds to one sample, which means that 
    multiple entries can point to a single patient.
    """

    all_data= list()
    service = get_unauthorized_service()

    for bcode in bcodes:
        data = service.samples().get(sample_barcode=bcode).execute()
        all_data.append(data)

    return all_data

# all_data in this case is a list of dictionaries
# Each dictionary corresponds to one barcode
# For most dicts, these are the keys (a couple are missing a field):
# [u'kind', u'patient', u'data_details', u'data_details_count', u'etag', u'aliquots', u'biospecimen_data'] 

# all_data[1]['data_details'][2]['cloud_storage_path']    < give a path to a file

# The number '2' designates a file. 


def get_dtypes(all_data, num):
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

def parse_cohort(cohort_ftext):
    """
    Removes samples from a response (the output of get_cohort).
    """

    buf = cohort_ftext.split("samples")[1]
    buf = buf.split("]")[0]
    res = re.findall('TCGA.*"', buf) #Looks for barcodes 
                     # under 'samples' in json format
    res = [x.replace('"','') for x in res]
    return res

def cohort_dstats(c_mdata):
    """
    Should count the number of each filetype that's available in the
    cohort
    """
    big_list  = []
    p_i       = 0

    for pdata in c_mdata:
        big_list.append('>>> ' + str(pdata['patient']))
        p_i += 1

def fetch(bcs):
    """
    Choose a fetch depending on whether barcodes are patient or 
    sample barcodes. Patient barcodes are shorter by three digits 
    and a dash, should be len=12 for patient and 16 for samples.
    """
    return fetch_patients(bcs) if len(bcs[0])<14 else\
           fetch_csamples(bcs)

def usage():

    usage = 'Usage: extractsamples.py '
    args  = '[-s/-p] [barcode_file]'
    print 
    print usage + args
    print 
    print '''Options:
    -s      Samples barcodes as input
    -p      Patient barcodes as input
         ''' 
    exit(1)



if __name__=='__main__':

    isb_auth.get_credentials()

    if len(sys.argv)!=3:
        usage()
    if sys.argv[1]!=('-s' or '-p'):
        usage()
    
    inp = open(sys.argv[-1])
    inpt= inp.read()

    res = parse_cohort(inpt) # res represents barcodes
    mdata = fetch(res)       # Mdata is a list of dicts
    # tmp = cohort_dstats(mdata)
    # d0  = cmdata.cmdata(mdata)
    import cmdata
    a0  = cmdata.cm(mdata, res)
    a0.write_download_script()
    import pdb;pdb.set_trace()



