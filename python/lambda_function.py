import io
import os
import sys
import json
import boto3
import logging

# DB Table 조회 후 class 생성
os.system("sqlacodegen {} > tables.py".format(os.environ['DB_INFO']))
from tables import *

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
    names = list(map(lambda x: '.'.join(x.split('.')[:-1]), names))

    result = {}
    if globals()['EXCEL_FORMAT'].get(names[0]):
        excel_format = globals()['EXCEL_FORMAT'][names[0]]

        if names[1]:
            excel_format = excel_format[names[1]]
        else:
            excel_format = list(excel_format.values())[0]

        for k, v in excel_format.items():
            if v != '':
                result[v] = data.loc[:, data.iloc[0, :] == k]

    return result


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

    results = []
    for k, v in data.items():
        t_name, c_name = k.split('.')
        results.append(globals()[t_name.capitalize()](api_name=n, service_num=i) for i, n in enumerate(v))

    with Session(engine) as session:
        session.bulk_save_objects(results[1:])
    #    api = session.query(globals()[t_name.capitalize()]).all()
    #    print(api)
    #    print(Api.__dict__.keys())

        # deleteList = tables.Api(
        #     api_name = "deleteList",
        #     service_num = 1
        # )

    #    for i in range(3):
    #        session.saveorupdate(globals()['test{}'.format(i)], unique_key = "api_name")
        session.commit()

    #
    engine.close()


if __name__ == '__main__':
    event = '/Users/mzc01-taehyun/k1m743hyun/excel-to-mysql/python/input/1. IPTV 미디어플랫폼 전환_DDD설계.xlsx - DDD설계 대상.csv'
    #event = '/Users/mzc01-taehyun/k1m743hyun/excel-to-mysql/python/input/1. IPTV 미디어플랫폼 전환_DDD설계.xlsx'
    _context = ''
    lambda_handler(event, _context)
