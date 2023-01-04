import datetime
import io
import os
import sys
import boto3
import logging

# DB Table 조회 후 class 생성
os.system("sqlacodegen {} > tables.py".format(os.environ['DB_INFO']))
import tables

# 서드파티 라이브러리 사용을 위한 경로 지정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages'))
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# logging을 위해 선언한 코드
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class Data:
    bucket_name = ''
    file_name = ''

    def __init__(self, event):
        # s3에 저장된 excel 파일 읽기를 위한 필요 정보 추출
        # Data.bucket_name = event['Records'][0]['s3']['bucket']['name']
        # Data.file_name = event['Records'][0]['s3']['object']['key']

        # 로컬에 저장된 excel 경로
        Data.file_name = event

    def read_s3_object(bucket_name, file_name):
        return boto3.client('s3').get_object(Bucket=bucket_name, Key=file_name)


class CSV(Data):
    data = None

    def __init__(self):
        CSV.data = pd.read_csv(Data.file_name, header=None)


class Excel(Data):
    data = None

    def __init__(self):
        Excel.data = pd.read_excel(Data.file_name, header=None, sheet_name=None)


class DDD(CSV, Excel):
    pass


def read_s3_object(bucket_name, file_name):
    #
    obj = boto3.client('s3').get_object(Bucket=bucket_name, Key=file_name)

    #
    data = None

    #
    try:
        # 확장자가 csv인 경우
        if obj['ContentType'] == 'text/csv':
            data = pd.read_csv(obj['Body'])

        # 확장자가 xls인 경우
        elif obj['ContentType'] == 'application/vnd.ms-excel':
            data = pd.read_excel(io.BytesIO(obj['Body'].read()))

        # 확장자가 xlsx인 경우
        elif obj['ContentType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            data = pd.read_excel(io.BytesIO(obj['Body'].read()))

    #
    except Exception as e:
        print(e)

    return data

def read_local_file(file_name):
    #
    data = None

    #
    try:
        # 확장자가 csv인 경우
        if '.csv' in file_name:
            data = pd.read_csv(file_name, header=None)

        # 확장자가 xls, xlsx인 경우
        elif '.xls' in file_name:
            data = pd.read_excel(file_name, header=None, sheet_name=None)

    #
    except Exception as e:
        print(e)

    return data

def parse_excel(data):
    # 값 없는 컬럼 삭제
    for column in data.columns:
        # 컬럼 값이 모두 NaN인 경우 삭제
        if data[column].count() == 0:
            data = data.drop(column, axis=1)

    # 값 없는 로우 삭제
    for row in data.index:
        # 로우 값이 모두 NaN인 경우 삭제
        if data.loc[row, :].count() == 0:
            data = data.drop(row, axis=1)

    # header 결정하기
    for row in data.index:
        # 로우 값이 모두 NaN이 아닌 경우 header로 결정
        if data.loc[row, :].isna().sum() == 0:
            data = data.iloc[row:, :]
            break

    return data


# # JSON 파일을 읽어서 전역 변수로 자동 생성
# for filename in os.listdir('json'):
#     if filename.split('.')[0]:
#         with open('json/{}'.format(filename), 'r') as json_file:
#             globals()[filename.split('.')[0].upper()] = json.load(json_file)


def lambda_handler(event, _context):
    obj = Data(event)

    # 확장자가 csv인 경우
    if obj['ContentType'] == 'text/csv':
        data = pd.read_csv(obj['Body'])

    # 확장자가 xls인 경우
    elif obj['ContentType'] == 'application/vnd.ms-excel':
        data = pd.read_excel(io.BytesIO(obj['Body'].read()))

    # 확장자가 xlsx인 경우
    elif obj['ContentType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        data = pd.read_excel(io.BytesIO(obj['Body'].read()))

    if '.csv' in data.file_name:
        f = CSV()
    elif '.xls' in data.file_name:
        f = Excel()

    print(f.file_name)


    # s3에 저장된 excel 파일 읽기
    #data = read_s3_object(bucket_name, file_name)
    # 로컬에 저장된 excel 파일 읽기
    data = read_local_file(f.file_name)

    # excel 파일 파싱하기
    data = parse_excel(data)

    #
    engine = create_engine(os.environ['DB_INFO'], echo=True).connect()

    #for i in range(3):
    #    globals()['test{}'.format(i)] = tables.Api(api_num = i+4, api_name="test{}".format(i), service_num=i+1)

    with Session(engine) as session:
        api = session.query(tables.Api).filter_by(api_name="deleteList")
        print(tables.Api.__dict__.keys())

        # deleteList = tables.Api(
        #     api_name = "deleteList",
        #     service_num = 1
        # )

    #    for i in range(3):
    #        session.saveorupdate(globals()['test{}'.format(i)], unique_key = "api_name")
    #    session.commit()

    #
    engine.close()


if __name__ == '__main__':
    event = ''
    _context = ''
    lambda_handler(event, _context)
