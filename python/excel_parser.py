import io
import os
import sys
import json
import boto3

# 서드파티 라이브러리 사용을 위한 경로 지정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages'))
import pandas as pd


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


def parse_data(names, data):

    # JSON 파일을 읽어서 전역 변수로 자동 생성
    with open('excel_format.json', 'r') as json_file:
        excel_format = json.load(json_file)

    names = list(map(lambda x: '.'.join(x.split('.')[:-1]), names))

    # JSON 파일에서 테이블 명과 컬럼 명 추출
    result = {}
    if excel_format.get(names[0]):
        excel_format = excel_format[names[0]]

        if names[1]:
            excel_format = excel_format[names[1]]
        else:
            excel_format = list(excel_format.values())[0]

        for k, v in excel_format.items():
            for i in v:
                result[i] = data.loc[:, data.iloc[0, :] == k]

        print(result)

    return result
