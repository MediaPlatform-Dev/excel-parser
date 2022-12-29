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

    try:
        if obj['ContentType'] == 'text/csv':
            df = pd.read_csv(obj['Body'])
        elif obj['ContentType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(obj['Body'].read()))

        print(df.iloc[:5, :])
    except Exception as e:
        print(e)

    print('finish')

