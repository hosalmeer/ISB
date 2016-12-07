from argparse import ArgumentParser
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import pprint
import os
from google.cloud import bigquery
import isb_auth
import requests
import isb_curl

# Need to set GOOGLE_APPLICATION_CREDENTIALS environment variable

# parse an input BQ table name
#     tableName should be of the form <gcp-project>:<dataset-name>.<table-name>
#                                  or <dataset-name>.<table-name>

project = "exemplary-point-148206"
# cmd = "ls -l"
# cmd = "export GOOGLE_APPLICATION_CREDENTIALS=./MFP-71e034b79ccf.json"

# must run in bash: 
# "export GOOGLE_APPLICATION_CREDENTIALS=/home/hos/workspace/SidraCancer/code/MFP-71e034b79ccf.json"

# MFP-71e034b79ccf.json is the name of the file with the credential

def list_tables(dataset_name, project=None):
    """Lists all of the tables in a given dataset.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset = bigquery_client.dataset(dataset_name)

    if not dataset.exists():
        print('Dataset {} does not exist.'.format(dataset_name))
        return

    for table in dataset.list_tables():
        print(table.name)

list_tables("isb-cgc:tcga_201510_alpha", project)


