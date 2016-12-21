
'''
A class defined to store cohort metadata. This is the second layer in
getting at the actual data files. The first layer is getting the 
base information about the cohort that we have already saved in TCGA.

That base information needs to be retrieved by the 'get_cohort' 
function. The response sends back a json format file which has 
barcodes for each patient, and a barcode for each biological sample.

Note that some patients have multiple samples.

Second class fits into the first class as ONE item from the cohort.
'''


class cm:

    def __repr__(self):
        return "Cohort of %s "

    def __init__(self, resp, barcodes=None):
        '''
        Initialise by passing in the response of fetch(). Only works
        with sample barcodes (not patient).
        '''
        self.all    = list()
        self.length = len(resp)

        if barcodes:
            for s in range(len(resp)):

                tmp = sample(resp[s], barcodes[s])
                self.all.append(tmp)

        else:
            for s in range(len(resp)):

                tmp = sample(resp[s])
                self.all.append(tmp)

class sample:
    '''
    Each sample has seven keys. Each samples has multiple files. 
    '''
    def __init__(self, sampledict):

        self.kind    = sampledict['kind']
        self.patient = sampledict['patient']
        self.fcount  = sampledict['data_details_count']
        self.etag    = sampledict['etag']
        self.aliquots= sampledict['aliquots']
        self.biospecimen_data = sampledict['biospecimen_data']
        self.__dd__  = sampledict['data_details']
        
        self.files   = list()
        for dd in self.__dd__:
            self.files.append(fdata(dd))  
        return
        
    
class fdata:
    '''
    Stores data for the individual file OF WHICH EACH BIOSAMPLE CAN
    HAVE MULTIPLE. Takes in a dict as input, one dict per file.
    '''

    def __init__(self, inp):
        '''
        There are variations in the fields here, so need to 
        '''

        # Mandatory fields, I don't think any datafile should be
        # missing these
        self.fields = inp.keys()
        self.SampleBarcode = inp['SampleBarcode']
        self.Datatype      = inp['Datatype']
        self.filepath = inp['cloud_storage_path']
        self.DataFileName  = inp['DataFileName']
        self.DataFileNameKey= inp['DataFileNameKey']
        self.SecurityProtocol = inp['SecurityProtocol']

        # Putting in Nones might be a bad idea tbh
        # since it makes it look like something's there

        try:
            self.DataCenterName= inp['DataCenterName']
        except KeyError:
            self.DataCenterName= None
        try:
            self.Pipeline      = inp['Pipeline']
        except KeyError:
            self.Pipeline      = None
        try:
            self.Repository    = inp['Repository']
        except KeyError:
            self.Repository    = None
        try:
            self.DatafileUploaded = inp['DatafileUploaded']
        except KeyError:
            self.DatafileUploaded = None
        try:
            self.DataCenterType= inp['DataCenterType']
        except KeyError:
            self.DataCenterType= None
        try:
            self.Project       = inp['Project']
        except KeyError:
            self.Project       = None
        try:
            self.Platform      = inp['Platform']
        except KeyError:
            self.Platform      = None
        try:
            self.DataLevel     = inp['DataLevel']
        except KeyError:
            self.DataLevel     = None
        try:
            self.SDRFFileName  = inp['SDRFFileName']
        except KeyError:
            self.SDRFFileName  = None

