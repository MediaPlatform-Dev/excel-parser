import io
import os
import sys
import boto3

# Thirdparty Libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages'))

import pandas as pd
from sqlalchemy import create_engine


class Excel:
    def __init__(self, event):
        # s3에 저장된 excel 파일 읽기를 위한 필요 정보 추출
        # self.bucket_name = event['Records'][0]['s3']['bucket']['name']
        # self.file_name = event['Records'][0]['s3']['object']['key']

        # 로컬에 저장된 excel 경로
        self.file_name = event

        #
        self.data = None


    def read_s3_object(self):
        #
        obj = boto3.client('s3').get_object(Bucket=self.bucket_name, Key=self.file_name)

        #
        try:
            # 확장자가 csv인 경우
            if obj['ContentType'] == 'text/csv':
                self.data = pd.read_csv(obj['Body'])

            # 확장자가 xls인 경우
            elif obj['ContentType'] == 'application/vnd.ms-excel':
                self.data = pd.read_excel(io.BytesIO(obj['Body'].read()))

            # 확장자가 xlsx인 경우
            elif obj['ContentType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                self.data = pd.read_excel(io.BytesIO(obj['Body'].read()))

        #
        except Exception as e:
            print(e)


    def read_local_file(self):
        #
        try:
            # 확장자가 csv인 경우
            if '.csv' in self.file_name:
                self.data = pd.read_csv(self.file_name, header=None)

            # 확장자가 xls, xlsx인 경우
            elif '.xls' in self.file_name:
                self.data = pd.read_excel(self.file_name, header=None)

        #
        except Exception as e:
            print(e)


    def parse_excel(self):
        # 값 없는 컬럼 삭제
        for column in self.data.columns:
            # 컬럼 값이 모두 NaN인 경우 삭제
            if self.data[column].count() == 0:
                self.data = self.data.drop(column, axis=1)

        # 값 없는 로우 삭제
        for row in self.data.index:
            # 로우 값이 모두 NaN인 경우 삭제
            if self.data.loc[row, :].count() == 0:
                self.data = self.data.drop(row, axis=1)

        # header 결정하기
        for row in self.data.index:
            # 로우 값이 모두 NaN이 아닌 경우 header로 결정
            if self.data.loc[row, :].isna().sum() == 0:
                self.data = self.data.iloc[row:, :]
                break


def connect_db(user, pwd, host, port, db_name):
    return create_engine(f'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db_name}').connect()


def disconnect_db(conn):
    conn.close()

def save_mysql():
    return 0


def lambda_handler(event, _context):
    # excel instance 생성
    excel = Excel(event)


    # s3에 저장된 excel 파일 읽기
    #excel.read_s3_object()
    # 로컬에 저장된 excel 파일 읽기
    excel.read_local_file()

    # excel 파일 파싱하기
    excel.parse_excel()

    #
    conn = connect_db('', '', 'localhost', 80, '')


    #
    disconnect_db(conn)


if __name__ == '__main__':
    event = ''
    _context = ''
    lambda_handler(event, _context)
