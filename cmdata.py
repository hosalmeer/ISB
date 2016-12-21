
'''
A class defined to store cohort metadata. This is the second layer in
getting at the actual data files. The first layer is getting the 
base information about the cohort that we have already saved in TCGA.

That base information needs to be retrieved by the 'get_cohort' 
function. The response sends back a json format file which has 
barcodes for each patient, and a barcode for each biological sample.

Note that some patients have multiple samples.
'''


class cmdata:
    def __init__(self, resp):
        self.i=1
        self.j=first

