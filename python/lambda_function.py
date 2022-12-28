import os
import sys
import boto3

# Thirdparty Libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages'))


class Excel:
    def __init__(self, event):
        self.bucket_name = event['Records'][0]['s3']['bucket']['name']
        self.file_name = event['Records'][0]['s3']['object']['key']

    def get_s3_object(self):
        return boto3.client('s3').get_object(self.bucket_name, self.file_name)


def lambda_handler(event, _context):
    excel = Excel(event)

    print(excel.bucket_name)
    print(excel.file_name)

    data = excel.get_s3_object()
    print(data)