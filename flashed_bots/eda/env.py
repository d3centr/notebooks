import os
import boto3
import s3fs
import json
import numpy as np
import pandas as pd
from pprint import pprint
from time import time
import random
from copy import deepcopy

DAY = '2022-12-13'
FIRST_BLOCK = 16172064
LAST_BLOCK = 16179214
REGION = os.environ['AWS_REGION'] 
SINK = os.environ['PLAYGROUND_BUCKET']
account_id = boto3.client('sts').get_caller_identity().get('Account')
bucket = f"dap-{REGION}-client-{account_id}"
traces = f'data/{REGION}/traces/prepost/date={DAY}'

s3, s3fs = boto3.resource('s3'), s3fs.S3FileSystem()
def load(block):
    if s3fs.exists(f'{bucket}/{traces}/{block}.json'):
        return json.loads(s3.Object(bucket, f'{traces}/{block}.json').get()['Body'].read())
    else:
        return []