import os
import sys
import boto3

# Thirdparty Libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages'))

import pandas as pd


def parse_excel():
    return ''

def lambda_handler(event, _context):
    parse_excel()


if __name__ == '__main__':
    event = ''
    _context = ''
    lambda_handler(event, _context)