import io
import os
import sys
import json
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

# JSON 파일을 읽어서 전역 변수로 자동 생성
with open('excel_format.json', 'r') as json_file:
    globals()['EXCEL_FORMAT'] = json.load(json_file)


def parse_data(names, data):


    return data


def preprocess_data(data):
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


def extract_file_name(file_name):
    # 파일 명만 추출
    file_name = file_name.split('/')[-1]

    # 확장자 추출
    extension = file_name.split('.')[-1]

    # 시트 명 추출
    split_name = file_name.split(' - ')
    len_split_name = len(split_name)

    if extension == 'csv' or 'xls' in extension:
        if len_split_name == 1:
            return extension, split_name + ['']

        elif len_split_name == 2:
            return extension, split_name

        else:
            return extension, [' - '.join(split_name[:-1]), split_name[-1]]

    else:
        return extension, [' - '.join(split_name), '']


def get_s3_object(bucket_name, file_name):
    return boto3.client('s3').get_object(Bucket=bucket_name, Key=file_name)


def read_data(bucket_name, file_name, extension):
    # obj 변수 초기화
    obj = None

    # s3에 저장된 excel 파일 읽기
    if bucket_name:
        obj = get_s3_object(bucket_name, file_name)

    # 확장자가 csv인 경우
    if extension == 'csv':
        # s3에서 excel 파일 읽은 경우
        if obj is not None:
            return pd.read_csv(obj['Body'], header=None)

        # 로컬에서 excel 파일 읽은 경우
        else:
            return pd.read_csv(file_name, header=None)

    # 확장자가 xls 또는 xlsx인 경우
    elif 'xls' in extension:
        # s3에서 excel 파일 읽은 경우
        if obj:
            return pd.read_excel(io.BytesIO(obj['Body'].read()), header=None)

        # 로컬에서 excel 파일 읽은 경우
        else:
            return pd.read_excel(file_name, header=None)

    # 나머지 확장자의 경우
    else:
        print("This is NOT supported")
        return 0


def lambda_handler(event, _context):
    # s3에 저장된 excel 파일 위치 정보 추출
    # bucket_name = event['Records'][0]['s3']['bucket']['name']
    # file_name = event['Records'][0]['s3']['object']['key']

    # 로컬에 저장된 excel 파일 경로
    bucket_name = None
    file_name = event

    # 확장자 및 시트 명 추출
    extension, names = extract_file_name(file_name)

    # excel 파일 읽기
    data = read_data(bucket_name, file_name, extension)

    # excel 데이터 전처리
    data = preprocess_data(data)

    # excel 데이터 파싱
    data = parse_data(names, data)

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
