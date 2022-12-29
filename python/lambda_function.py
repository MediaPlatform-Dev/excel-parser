import io
import os
import sys
import boto3

# Thirdparty Libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages'))

import pandas as pd

def lambda_handler(event, _context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    obj = boto3.client('s3').get_object(Bucket=bucket_name, Key=file_name)
    print(obj)

    if obj['ContentType'] == 'text/csv':
        df = pd.read_csv(obj['Body'])
        print(df.iloc[:5, :])
    elif obj['ContentType'] == ('application/vnd.ms-excel' or 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        df = pd.read_excel(obj['Body'])
        print(df.iloc[:5, :])

    print('finish')

